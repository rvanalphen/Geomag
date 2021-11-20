
import timeit   
from pathlib import Path, PosixPath
from typing import Dict, Union
from matplotlib import lines
from pandas.core.frame import DataFrame
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.seperate_data import DistanceSperator
from source.export_data import ExportPatch,ExportLines,ExportAll
from source.cut_data import NorthSouthCut,EastWestCut
import os
from pandas import merge
from functools import reduce
import matplotlib.pyplot as plt 
from scipy.spatial.distance import cdist
from numpy import linspace

#TODO fix recursive folder creation
######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/cleaned_data'
FILE = Path(f'{DATA_DIR}/All_NS_processedOn_2021_11_17.csv')# north - south lines
# FILE = Path(f'{DATA_DIR}/20191021_224036.txt')# east - west lines
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-18', '2019-10-17',  '2019-10-19', '2019-10-21']
ELEVATION = '0'

####################### - Helper Functions - ######################
 
def files_to_dict(dirpath: Union[PosixPath,str]) -> Dict:
    num = 0
    files_dict = {}
    for filename in os.listdir(dirpath):
        if '.' in filename and\
             '20191021_170314.txt' not in filename\
                 and '20191022_003746.txt' not in filename: 
            num += 1
            fullpath = Path(dirpath+filename)
            files_dict[str(num)] = fullpath

    return files_dict

def merge_object_data(dictionary: Dict) -> DataFrame:
    data_list =[]
    for key,value in dictionary.items():
        data_list.append(
            dictionary[key])

    return reduce(lambda left, right: merge(left, right, how='outer'), data_list)


def closest_point(point:list[Union[int,float]], points: list[Union[int,float]]) -> tuple:
    """ Find closest point from a list of points. """
    return points[cdist([point], points).argmin()]

def get_line(data: DataFrame,start: list[Union[int,float]], end: list[Union[int,float]]) -> DataFrame:
    data = data[['Easting','Northing','Mag_nT']]
    df1 = DataFrame()
    df1['point'] = [(x, y) for x,y in zip(data['Easting'],data['Northing'])]
    
    x = linspace(start[0],end[0],endpoint=True,num = 100)
    y = linspace(start[1],end[1],endpoint=True,num = 100)

    df2 = DataFrame()
    df2['point'] = [(x, y) for x,y in zip(x, y)]
    
    closest = DataFrame()
    closest['Easting'],closest['Northing'] = list(zip(*[closest_point(x, list(df1['point'])) for x in df2['point']]))
    closest['Mag_nT'] = data['Mag_nT']

    return closest

######################### - Main - ###############################
# start = [536126.5,4070411]
# end = [536164,4068755]
# start = [534641,4070410]
# end = [534678,4068732]
def main():

    print(FILE,'\n')
    # initializing and validating input parameters
    geomag = GeoMag(
        filepath=FILE,
        input_epsg=INEPSG,
        output_epsg=OUTEPSG,
        dates=DATES,
        elevation=ELEVATION
    )

    # creating new App instance with all cleaned data
    app = App(parameters = geomag)
    plot = DataPlotter()




    
    get_line(app.data,start,end)

    # fig, ax = plt.subplots(figsize=(10, 10))
    # ax.scatter(x=start[0],y=start[1])
    # ax.scatter(x=end[0],y=end[1])
    # for i,_ in enumerate(closest):
    #     ax.scatter(closest[i][0],closest[i][1],linestyle='None', marker="o", s=10)
    # plt.show()

    # plot.simple_plot(app)


if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))
