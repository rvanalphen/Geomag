
import timeit   
from pathlib import Path, PosixPath
from typing import Dict, Union
from matplotlib import lines
import pandas
from pandas.core.frame import DataFrame
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.seperate_data import DistanceSperator
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


    print('Starting cropping lines')
    #bb = bottom bound, tb = top bound, the bounds between a single line
    lb =-116.6140
    rb = -116.6138

    # the incriment I want to shift the bounds by 

    ic = 0.0004

    # the number I dont want my bounds to go pass 
    limit = -116.595

    #creating a list for the bb and tb to go into 
    lb_list = []
    rb_list = []


    #the two while loops that incriments my two bounds and then puts them into a list  
    print('left')
    while lb< 0:
    #   print (lb)
        lb= lb+ ic
        lb_list.append(lb)
        if lb> limit:
            break
    print ('Done')


    print('right')
    while rb< 0:
    #  print (rb)
        rb= rb+ ic
        rb_list.append(rb)
        if rb> limit:
            break
    print ('Done')

    # cutting each line and assiging it a dataframe 
    line_1 = app.data[(app.data.Long >  -1116.6140) & (app.data.Long <  -116.6138)]
    line_2 = app.data[(app.data.Long >  lb_list[0]) & (app.data.Long <  rb_list[0])]
    line_3 = app.data[(app.data.Long >  lb_list[1]) & (app.data.Long <  rb_list[1])]
    line_4 = app.data[(app.data.Long >  lb_list[2]) & (app.data.Long <  rb_list[2])]
    line_5 = app.data[(app.data.Long >  lb_list[3]) & (app.data.Long <  rb_list[3])]

    l5 = pandas.read_csv('./Line_5_det.in',sep=' ',names=['e','n','m'])
    print(l5)



    fig, ax = plt.subplots(figsize=(10, 10))
    
    # ax.plot(app.data.Easting,app.data.Northing,'o')

    ax.plot(l5.n, l5.m,'o',color='black')

    ax.plot(line_5.Northing, line_5.Mag_nT,'o',color='red')
    
    plt.show()



if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))
