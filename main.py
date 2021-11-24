
import timeit   
from pathlib import Path
import pandas

from pandas.core.frame import DataFrame
from source.export_data import ExportLines
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.separate_data import SingleSeparator
from source.correct_data import NorthSouthDetrend
from source.model_data import PloufModel
import matplotlib.pyplot as plt

#TODO fix recursive folder creation
######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/cleaned_data/cleaned_lines/'
SHAPE_DIR = '/home/robert/Codes/pycodes/geomag/shapes/'

FILE = Path(f'{DATA_DIR}/All_NS_processedOn_2021_11_17_line 1_processedOn_2021_11_23.csv')# north - south lines
# FILE = Path(f'{DATA_DIR}/20191021_224036.txt')# east - west lines
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-18', '2019-10-17',  '2019-10-19', '2019-10-21']
ELEVATION = '0'

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
    )

    # creating new App instance with all cleaned data
    app = App(parameters = geomag)
    app.data = app.data[app.data.Northing < 4069900]
    app.data_is_line()

    plouf = PloufModel(
        line = app.lines['line 1'],
        shapes= [Path(f'{SHAPE_DIR}/shape3.utm')],
        top_bound= [45.5],
        bottom_bound= 55,
        inclination= -67,
        declination= 177,
        intensity= 0.5
    )

    model_dict = plouf.run_model()
    print(app.lines['line 1'])
    print(len(model_dict['df_model1']))


    fig, ax = plt.subplots(figsize=(10, 10))

    ax.plot(app.lines['line 1'].Northing,app.lines['line 1'].Mag_nT,'go',ms=2,label='Observed')

    for key in model_dict.keys():
        ax.plot(model_dict[key].dist,model_dict[key].mag,'r-',ms=2,label='Calculated(plouf)')

    ax.set_xlabel('Horizontal distance north from line center')
    ax.set_ylabel('Magnetic Anomaly (nT)')
    ax.legend(loc='lower left')
    plt.show()





    






if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))
