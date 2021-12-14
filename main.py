
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


DATA_DIR = './'

FILE = Path(f'{DATA_DIR}/20191019_235522_line 1_processedOn_2021_12_05.csv')# north - south lines
INEPSG = '4326'
OUTEPSG = '32611'
DATES = ['2019-10-20']
# ['2019-10-18', '2019-10-17',  '2019-10-19', '2019-10-21']
# ELEVATION = '0'

######################### - Main - ###############################
import numpy as np
import matplotlib.pyplot as plt 

def DFT(x):
    """
    Function to calculate the 
    discrete Fourier Transform 
    of a 1D real-valued signal x
    """

    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    
    X = np.dot(e, x)
    
    return X



def main():

    geomag = GeoMag(
        filepath=FILE,
    )

    app = MagApp(parameters=geomag)
    app.data_is_line()


if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n',FILE)
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))

