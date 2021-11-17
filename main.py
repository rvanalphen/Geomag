
import timeit   
from pathlib import Path
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.seperate_data import DistanceSperator
from source.export_data import ExportPatch,ExportLines,ExportAll
import os
from pandas import merge
from functools import reduce
######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/'
# FILE = Path(f'{DATA_DIR}/20191019_184358.txt')# north - south lines 
# FILE = Path(f'{DATA_DIR}/20191021_224036.txt')# east - west lines
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-18', '2019-10-17',  '2019-10-19', '2019-10-21']
ELEVATION = '0'

######################### - Main - ###############################

def files_to_dict(dirpath):
    num = 0
    files_dict = {}
    for filename in os.listdir(dirpath):
        if '.' in filename and '20191021_170314.txt' not in filename:
            num += 1
            fullpath = Path(dirpath+filename)
            files_dict['File '+str(num)] = fullpath
    return files_dict

def merge_object_data(dictionary):
    data_list =[]
    for key,value in dictionary.items():
        data_list.append(
            dictionary[key])

    return reduce(lambda left, right: merge(left, right, how='outer'), data_list)


def main():
    
    all_files = files_to_dict(DATA_DIR)
    object_dict={}

    for KEY,FILE in all_files.items():
    
        print(FILE,'\n')
        # initializing and validating input parameters
        geomag = GeoMag(
            filepath=FILE,
            input_epsg=INEPSG,
            output_epsg=OUTEPSG,
            dates=DATES,
            elevation=ELEVATION
        )

        # create the application and plotting class
        app = App(parameters = geomag)

        plotter = DataPlotter()

        # transforming lat long to utm
        app.transform_coords()

        # cleaning data based on input strategey
        app.cut_data()

        # getting only the local field values  - value=48488
        app.subtract_total_field()

        # putting each objects data into a list for merging 
        object_dict[KEY] = app.data

    # merging each files cleaned data into one DataFrame
    merged_data = merge_object_data(object_dict)

    # creating new App instance with all cleaned data
    app = App(merged_patches = merged_data)

    # seperating each line into a dict under app.lines
    app.separate_lines(DistanceSperator())

    plotter.plot_mag_profile(app,key_name='line_10')




if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))

    # exporting the changed data depending on strategy employed
    # app.export_data(ExportAll())

    # plotting individual lines

    # plotting each magnetic profile with an offset
    # plotter.plot_offset_profile(app)