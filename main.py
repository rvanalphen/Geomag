
import timeit   
from pathlib import Path, PosixPath
from typing import Dict, Union
from matplotlib import lines
import pandas
from pandas.core.frame import DataFrame
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.seperate_data import DistanceSperator,SingleSeparator
from source.export_data import ExportPatch,ExportLines,ExportAll
from source.cut_data import NorthSouthCut,EastWestCut
from source.helper_functions import merge_object_data,closest_point,get_line,files_to_dict
import os
from pandas import merge
from functools import reduce
import matplotlib.pyplot as plt 
from scipy.spatial.distance import cdist
from numpy import linspace

#TODO fix recursive folder creation
######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/cleaned_data'
FILE = Path(f'{DATA_DIR}/All_NS_samespacing_processedOn_2021_11_17.csv')# north - south lines
# FILE = Path(f'{DATA_DIR}/20191021_224036.txt')# east - west lines
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-18', '2019-10-17',  '2019-10-19', '2019-10-21']
ELEVATION = '0'

def closest_point(point:list[Union[int,float]], points: list[Union[int,float]]) -> tuple:
    """ Find closest point from a list of points. """
    return points[cdist([point], points).argmin()]

def get_line(data: DataFrame,start: list[Union[int,float]], end: list[Union[int,float]]) -> DataFrame:
    data = data[['Easting','Northing','Mag_nT']]
    df1 = DataFrame()
    df1['point'] = [(x, y) for x,y in zip(data['Easting'],data['Northing'])]
    
    x = linspace(start[0],end[0],endpoint=True,num = 500)
    y = linspace(start[1],end[1],endpoint=True,num = 500)

    df2 = DataFrame()
    df2['point'] = [(x, y) for x,y in zip(x, y)]
    
    closest = DataFrame()
    closest['Easting'],closest['Northing'] = list(zip(*[closest_point(x, list(df1['point'])) for x in df2['point']]))
    return closest
######################### - Main - ###############################
# start = [536126.5,4070411]
# end = [536164,4068755]
# start = [534678,4068732]
# end = [534641,4070410]
# l5 = pandas.read_csv('./test.in',sep=' ',header=0)

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
    
    line_params = {
        'start': [534605.4451, 4068731.615],
        'end' : [534560.0319, 4070426.924],
        'buffer' : 10
    }

    app.separate_lines(SingleSeparator(),line_params)

    print(app.lines)


    # fig, ax = plt.subplots(figsize=(10, 10))
    
    # ax.plot(app.data.Easting,app.data.Northing,'o',ms=10)
    # ax.plot(app.lines.Easting,app.lines.Northing,'o',color='black',ms=5)
    # ax.plot([line_params['start'][0],line_params['end'][0]],
    #     [line_params['start'][1],line_params['end'][1]])

    # plt.show()


if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))
