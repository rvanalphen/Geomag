import timeit   
from pathlib import Path

from pyproj.transformer import transform
from source.correct_data import NorthSouthDetrend

from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.model_data import PloufModel
import matplotlib.pyplot as plt
from source.stats import Stats

######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/cleaned_data/'
FILE = Path(f'{DATA_DIR}/All_data_cleaned_processedOn_2021_11_28.csv')# north - south lines
INEPSG = '4326'
OUTEPSG = '32611'
######################### - Main - ###############################

def main():

    print(FILE,'\n')
    # initializing and validating input parameters
    geomag = GeoMag(
        filepath=FILE,
        input_epsg=INEPSG,
        output_epsg=OUTEPSG
    )

    # creating new App instance with all cleaned data
    app = App(parameters = geomag)

    plotter = DataPlotter()
    plotter.cartoplot(app,'survey points',length=500,segments=2)











if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))