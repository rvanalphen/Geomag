
#%%
import math
from re import L
import timeit   
from pathlib import Path
from numpy import mod

import pandas
from source.correct_data import NorthSouthDetrend
from source.plot_data import plot_model,plot_residuals
from source.geomag import GeoMag
from source.app import MagApp
from source.model_data import PloufModel
from source.stats import get_rmse,ks_test
import matplotlib.pyplot as plt
from sklearn.model_selection import ParameterGrid
#TODO fix recursive folder creation
#TODO write plotting functions to show cut line compared to whole
#TODO write plotting function to show cut line and shape
######################## - INPUTS - #############################

DATA_DIR = '/home/robert/Codes/pycodes/geomag/'
SHAPE_DIR = '/home/robert/Codes/pycodes/geomag/shapes/'

FILE = Path(f'{DATA_DIR}/20191019_235522_line 1_processedOn_2021_12_05.csv')# north - south lines
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


    param_grid = {
        'top':[[42],[40],[41],[43],[44],[45]],
        'bottom':[50,51,52,53,54,55],
        'intensity':[0.5,0.6,0.7,0.8,0.9,1]
        }

    grid_search = ParameterGrid(param_grid)
    print(len(list(grid_search)))


    all_models = []
    for i,grid in enumerate(grid_search):
        if i < 3:

            model = PloufModel(
                line = app.lines['line 1'],
                shapes= [Path(f'{SHAPE_DIR}/line_56a_shape2.utm')],
                top_bound= grid['top'],
                bottom_bound= grid['bottom'],
                inclination= -67,
                declination= 177,
                intensity= grid['intensity']
            )

            all_models.append(model)

    for model in all_models:

        print(model.Parameters)
        model.run_plouf()

        # print(grid)


if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))
# %%
