
import timeit   
from pathlib import Path
from source.load_data import path_to_df
from source.plot_data import plot_model,plot_residuals
from source.geomag import GeoMag
from source.app import MagApp
from source.model_data import PloufModel
from source.stats import get_abs_max_error, get_durban_watson, get_rmse,ks_test
from pprint import pprint
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

def main():

    print(FILE,'\n')
    # initializing and validating input parameters
    geomag = GeoMag(
        filepath=FILE,
    )

    # creating new MagApp instance with all cleaned data
    app = MagApp(parameters = geomag)
    app.data_is_line()

    line = app.lines['line 1']

    shape= path_to_df(Path(f'{SHAPE_DIR}/line_56a_shape6.utm'))

        
    grid_model = PloufModel(
        line = line,
        shape= shape,
        top_bound= 45,
        bottom_bound= 53,
        inclination= -67,
        declination= 177,
        intensity= 0.7
    )

    grid_model.run_plouf()

    print("Absolute Max Error: %f" % get_abs_max_error(grid_model))
    print("RMSE: %f" % get_rmse(grid_model))
    print("Durban-Watson Test (residuals): %f" % get_durban_watson(grid_model))

    plot_model(app,grid_model)
    plot_residuals(grid_model)
    ks_test(app,grid_model,bins=10)


if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))

