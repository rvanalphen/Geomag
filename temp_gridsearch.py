
import timeit   
from pathlib import Path
from source.load_data import path_to_df
from source.plot_data import plot_model,plot_residuals
from source.geomag import GeoMag
from source.app import MagApp
from source.model_data import PloufModel,grid_search
from source.stats import get_abs_max_error, get_rmse,ks_test
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
    
    shape = path_to_df(Path(f'{SHAPE_DIR}/line_56a_shape2.utm'))
    
    
    param_grid = {
        'top':[42,40,41,43,44,45],
        'bottom':[50,51,52,53,54,55],
        'intensity':[0.5,0.6,0.7,0.8,0.9,1]
        }
    
    current,good_grid = grid_search(line,shape,param_grid,get_rmse)
    print("\n")
    print('Final Grid: ',good_grid)
    print('Final Model RMSE: ',current)


    grid_model = PloufModel(
        line = line,
        shape= shape,
        top_bound= good_grid['top'],
        bottom_bound= good_grid['bottom'],
        inclination= -67,
        declination= 177,
        intensity= good_grid['intensity']
    )

    grid_model.run_plouf()


    print(get_abs_max_error(grid_model))
    print(get_rmse(grid_model))

    plot_model(app,grid_model)
    plot_residuals(grid_model)
    ks_test(app,grid_model,bins=10)

# {'bottom': 53, 'intensity': 0.8, 'top': [45]}


if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))

