
import timeit   
from pathlib import Path, PosixPath
from typing import Dict, Union

from pandas.core.frame import DataFrame
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.seperate_data import DistanceSperator, HistSeperator
from source.export_data import ExportPatch,ExportLines,ExportAll
from source.cut_data import NorthSouthCut,EastWestCut
import os
from pandas import merge
from functools import reduce
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

######################### - Main - ###############################

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

    # mag_sub_set =[]
    # utm_north_sub_set = []
    # for i in range(len(mag_set)):
    #     if (utm_east[i] > 307891) & (utm_east[i]< 307925):
    #         mag_sub_set.append(mag_set[i])
    #         utm_north_sub_set.append(utm_north[i])



if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))
