
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

    l5 = pandas.read_csv('./test.in',sep=' ',header=0)
    
    # start = [l5.Easting.max(),l5.Northing.min()]
    # end = [l5.Easting.min(),l5.Northing.max()]

    start = [534678,4068732]
    end = [534641,4070410]

    import geopandas as gpd
    import shapely.geometry

    dfp = gpd.GeoDataFrame(
        app.data,
        geometry=app.data.loc[:,["Easting","Northing"]].apply(shapely.geometry.Point, axis=1),
        crs="EPSG:32611",
    )
    
    line = shapely.geometry.LineString(
        [start,end]
    )
    # add a buffer to LineString (hence becomes a polygon)
    DISTANCE = 10 #m
    line = (
        gpd.GeoSeries([line], crs="EPSG:32611").buffer(DISTANCE)
    )
    
    df_near = gpd.GeoDataFrame(geometry=line).sjoin(dfp)
    df = df_near.iloc[:,2:]
    print(df)



    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.plot(app.data.Easting,app.data.Northing,'o',ms=10)
    # ax.plot(l5.Easting,l5.Northing,'o',color='black',ms=10)
    ax.plot(df.Easting,df.Northing,'o',color='black',ms=5)
    ax.plot([start[0],end[0]],[start[1],end[1]])

    plt.show()





    # # cutting each line and assiging it a dataframe 
    # line_1 = app.data[(app.data.Long >  -1116.6140) & (app.data.Long <  -116.6138)]
    # line_2 = app.data[(app.data.Long >  lb_list[0]) & (app.data.Long <  rb_list[0])]
    # line_3 = app.data[(app.data.Long >  lb_list[1]) & (app.data.Long <  rb_list[1])]
    # line_4 = app.data[(app.data.Long >  lb_list[2]) & (app.data.Long <  rb_list[2])]
    # line_5 = app.data[(app.data.Long >  lb_list[3]) & (app.data.Long <  rb_list[3])]





if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))
