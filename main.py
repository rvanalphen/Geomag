
#%%
from re import L
import timeit   
from pathlib import Path

import pandas
from source.correct_data import NorthSouthDetrend

from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import MagApp
from source.model_data import PloufModel
import matplotlib.pyplot as plt
from source.stats import Stats

#TODO fix recursive folder creation
#TODO write plotting functions to show cut line compared to whole
#TODO write plotting function to show cut line and shape
######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/cleaned_data/cleaned_lines/'
SHAPE_DIR = '/home/robert/Codes/pycodes/geomag/shapes/'

FILE = Path(f'{DATA_DIR}/All_NS_processedOn_2021_11_17_line 1_processedOn_2021_11_29.csv')# north - south lines
# FILE = Path(f'{DATA_DIR}/20191021_224036.txt')# east - west lines
# INEPSG = '4326'
# OUTEPSG = '32611'
# DATES = ['2019-10-18', '2019-10-17',  '2019-10-19', '2019-10-21']
# ELEVATION = '0'

######################### - Main - ###############################

#%%

def main():

    print(FILE,'\n')
    # initializing and validating input parameters
    geomag = GeoMag(
        filepath=FILE,
    )

    # creating new MagApp instance with all cleaned data
    app = MagApp(parameters = geomag)
    app.data_is_line()

    plotter = DataPlotter()
    statter = Stats()


    model = PloufModel(
        line = app.lines['line 1'],
        shapes= [Path(f'{SHAPE_DIR}/shape5.utm')],
        top_bound= [40],
        bottom_bound= 50,
        inclination= -67,
        declination= 177,
        intensity= 0.5
    )

    model.run_plouf()

    plotter.plot_model(app,model)
    statter.ks_test(app,model)    
    statter.rmse(app,model)
    statter.chi_squared(app,model)


if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))