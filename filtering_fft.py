
#TODO fix recursive folder creation
#TODO write plotting functions to show cut line compared to whole
#TODO write plotting function to show cut line and shape
######################## - INPUTS - #############################
import timeit
from pathlib import Path
from source.app import MagApp
from source.correct_data import EastWestDetrend
from source.export_data import ExportLines
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
from scipy.fftpack import fft, ifft,fftfreq

def main():

    geomag = GeoMag(
        filepath=FILE,
    )

    app = MagApp(parameters=geomag)
    app.data_is_line()

    #preping data 

    # this is the signal
    x = app.lines['line 1']['Mag_nT'].to_numpy()

    #length of the signal
    N = len(x)

    #sampling rate, rocco took ever second ie 1Hz
    sr = 1 
    
    # creating a time column 1 second per sample
    app.lines['line 1']['Time (s)'] = np.arange(0,N)
    t = app.lines['line 1']['Time (s)'].to_numpy()

    ##### fft stuff ############

    # getting fft 
    sig_fft = fft(x)
    # copy the FFT results
    sig_fft_filtered = sig_fft.copy()

    # obtain the frequencies using scipy function
    freq = fftfreq(len(x), d=1/sr)


    # define the cut-off frequency
    cut_off = 0.005

    sig_fft_filtered[np.abs(freq) > cut_off] = 0

    # get the filtered signal in time domain
    filtered = ifft(sig_fft_filtered)

    # get the one side frequency
    n_oneside = N//2
    freq_oneside = freq[:n_oneside]
    sig_fft_filtered_oneside = sig_fft_filtered[:n_oneside]
    sig_fft_onesided =sig_fft[:n_oneside]


    # plot the filtered signal with the original
    plt.figure(figsize = (12, 6))
    plt.plot(t, np.real(filtered))
    plt.plot(t, x, 'r')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()


    # plot the FFT amplitude before and after
    plt.figure(figsize = (12, 6))
    plt.subplot(121)
    plt.stem(freq_oneside, np.abs(sig_fft_onesided), 'b', \
            markerfmt=" ", basefmt="-b")
    plt.title('Before filtering')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('FFT Amplitude')
    plt.xlim(-0.005,0.02)

    plt.subplot(122)
    plt.stem(freq_oneside, np.abs(sig_fft_filtered_oneside), 'b', \
            markerfmt=" ", basefmt="-b")
    plt.title('After filtering')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('FFT Amplitude')
    plt.tight_layout()
    plt.xlim(-0.005,0.02)
    plt.show()



    app.lines['line 1']['filtered'] = np.real(filtered)

    app.export_data(export_strategy=ExportLines())

if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n',FILE)
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))

