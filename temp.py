
#TODO fix recursive folder creation
#TODO write plotting functions to show cut line compared to whole
#TODO write plotting function to show cut line and shape
######################## - INPUTS - #############################
import timeit
from pathlib import Path
from source.app import MagApp
from source.correct_data import EastWestDetrend
from source.geomag import GeoMag
from source.plot_data import plot_mag_profile, simple_plot
from source.separate_data import DistanceSperator
from source.stats import get_stats


DATA_DIR = './cleaned_lines'

FILE = Path(f'{DATA_DIR}/20191019_235522_line 1_processedOn_2021_12_05_line 1_processedOn_2021_12_13.csv')# north - south lines
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-20']
# ['2019-10-18', '2019-10-17',  '2019-10-19', '2019-10-21']
# ELEVATION = '0'

######################### - Main - ###############################
import numpy as np
import matplotlib.pyplot as plt 

def plot_filt(app: MagApp, key_name:str='line 1'):
    fig, ax = plt.subplots(figsize=(15, 5))

    data = app.lines[key_name]
    ax.plot(data.Northing, data.filtered, marker="o",
            linestyle='None', markersize=3)

    ax.set_xlabel("Northing")
    ax.set_ylabel("Magnetic Signal (nT)")

    ax.set_title(key_name)

    plt.show()


def main():

    geomag = GeoMag(
        filepath=FILE,
    )

    app = MagApp(parameters=geomag)
    app.data_is_line()

    plot_mag_profile(app,key_name='line 1')
    plot_filt(app,key_name='line 1')

    





    
if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n',FILE)
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))

