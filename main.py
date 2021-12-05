
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

    plotter = DataPlotter()
    statter = Stats()


    from source.helper_functions import files_to_dict
    from source.load_data import path_to_df

    shape_files = files_to_dict(SHAPE_DIR)

    shape_data={}
    for key,f in shape_files.items():
        shape_data[key] = path_to_df(f)



    # fig, ax = plt.subplots(figsize=(10, 10))

    # ax.plot(app.data.Easting,app.data.Northing,linestyle='None', marker="o", ms=2,c="k", label="Data line")
    # for key in shape_data.keys():
    #     ax.plot(shape_data[key].Easting,shape_data[key].Northing,
    #             linestyle='-', marker="o", ms=2,label=key)
    # ax.legend()
    # plt.show()




    model = PloufModel(
        line = app.lines['line 1'],
        shapes= [Path(f'{SHAPE_DIR}/line_56a_shape5.utm')],
        top_bound= [42],
        bottom_bound= 52,
        inclination= -67,
        declination= 177,
        intensity= 0.6
    )


    model.run_plouf()
    # rmse,norm_rmse = statter.rmse(app,model)
        
    plotter.plot_model(app,model)
    # plotter.plot_residuals(model)
    # print("RMSE: ",rmse)
    # print("Norm RMSE: ", norm_rmse)
    statter.ks_test(app,model)
    # statter.chi_squared(app,model)


if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))
# %%
