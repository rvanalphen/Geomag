
from pathlib import Path
from pyproj import Transformer, CRS
from re_geomag import GeoMag
from clean_data import DataCleaner
from load_data import path_to_df
from correct_data import MagCorrector
from plot_data import DataPlotter


######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/'
FILE = Path(f'{DATA_DIR}/20191019_184358.txt')
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-17', '2019-10-18', '2019-10-19', '2019-10-21']

######################### - Main - ###############################

def main():
    geomag = GeoMag(
        filepath= FILE,
        input_epsg = INEPSG,
        output_epsg = OUTEPSG,
        )

    #* turning file into a dataframe
    df = path_to_df(geomag.filepath)
    
    #* transforming lat long to utm
    transformer = Transformer.from_crs(geomag.input_epsg, geomag.output_epsg)
    df["Easting"],df["Northing"] = transformer.transform(df.Lat.values,df.Long.values)


    #* Correcting for the total field
    # magcorrector = MagCorrector()
    # magcorrector.global_detrend(df,value=48488)


    # #* cleaning up the data to keep only what I want
    # cleaner = DataCleaner()
    # cleaner.cut_heading(df,geomag.direction)

    # #* plotting the data
    # plotter = DataPlotter(df)
    # plotter.simple_plot()

    print(df)

if __name__ == "__main__":
    main()
