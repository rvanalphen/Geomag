
from pathlib import Path
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.seperate_data import DistanceSperator
from source.export_data import ExportPatch,ExportLines

######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/'
FILE = Path(f'{DATA_DIR}/20191019_184358.txt')# north - south lines 
# FILE = Path(f'{DATA_DIR}/20191021_231039.txt')# east - west lines
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-18', '2019-10-17',  '2019-10-19', '2019-10-21']
ELEVATION = 0

######################### - Main - ###############################


def main():

    # * initializing and validating input parameters
    geomag = GeoMag(
        filepath=FILE,
        input_epsg=INEPSG,
        output_epsg=OUTEPSG,
        dates=DATES,
        elevation=ELEVATION
    )

    # * create the application and plotting class
    app = App(geomag)
    plotter = DataPlotter()

    # * transforming lat long to utm
    app.transform_coords()
    # plotter.simple_plot(app.data)

    # # * cleaning data based on input strategey
    # app.cut_data()
    # # plotter.simple_plot(app.data)

    # # * getting only the local field values  - value=48488
    # app.subtract_total_field()

    # # * seperating each line into a dict under app.lines
    app.separate_lines(DistanceSperator())

    app.export_data(ExportLines())






    # * plotting individual lines
    # plotter.plot_mag_profile(app.parameters.filepath,app.lines,key_name='line 1')

    # * plotting each magnetic profile with an offset
    # plotter.plot_offset_profile(app.parameters.filepath,app.lines)

    # print(app.data)
    # for key in app.lines:
    #     print(key)
    #     print(app.lines[key])


if __name__ == "__main__":
    main()
