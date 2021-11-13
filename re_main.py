
from pathlib import Path

from pandas.core.frame import DataFrame
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.clean_data import NorthSouthCleaner


######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/'
FILE = Path(f'{DATA_DIR}/20191019_184358.txt')
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-17', '2019-10-18', '2019-10-19', '2019-10-21']

######################### - Main - ###############################


def main():

    # * initializing and validating input parameters
    geomag = GeoMag(
        filepath=FILE,
        input_epsg=INEPSG,
        output_epsg=OUTEPSG,
        date_range=DATES
    )

    # * create the application
    app = App(geomag)

    # * transforming lat long to utm
    app.transform_coords()

    # * cleaning data based on input strategey
    app.clean_data(NorthSouthCleaner())

    # * getting only the local field values
    app.subtract_total_field()

    plotter = DataPlotter(app.data)
    plotter.simple_plot()

    print(app.data)


if __name__ == "__main__":
    main()
