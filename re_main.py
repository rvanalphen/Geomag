
from pathlib import Path
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App


######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/'
FILE = Path(f'{DATA_DIR}/20191019_184358.txt')
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-17', '2019-10-18', '2019-10-19', '2019-10-21']
ELEVATION = 800

######################### - Main - ###############################


def main():

    # * initializing and validating input parameters
    geomag = GeoMag(
        filepath=FILE,
        input_epsg=INEPSG,
        output_epsg=OUTEPSG,
    )

    # * create the application
    app = App(geomag)

    # * transforming lat long to utm
    app.transform_coords()

    # * cleaning data based on input strategey
    app.cut_data()

    # * getting only the local field values
    app.subtract_total_field(value=48488)

    plotter = DataPlotter(app.data)
    plotter.simple_plot()
    

    # print(app.data)


if __name__ == "__main__":
    main()
