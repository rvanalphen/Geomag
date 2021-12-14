
#TODO fix recursive folder creation
#TODO write plotting functions to show cut line compared to whole
#TODO write plotting function to show cut line and shape
######################## - INPUTS - #############################
import timeit
from pathlib import Path

from matplotlib import scale
from source.app import MagApp
from source.correct_data import EastWestDetrend
from source.geomag import GeoMag
from source.plot_data import plot_mag_profile, simple_plot
from source.separate_data import DistanceSperator
from source.stats import get_stats


DATA_DIR = './cleaned_lines'

FILE = Path(f'{DATA_DIR}/Line_15_det_mod.in')# north - south lines
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
    plot_mag_profile(app,key_name='line 1',direction='NS')

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

    # obtain the frequencies using scipy function, d - inverse of sampling rate defaults to 1 
    freq = fftfreq(len(x), d=1/sr)

    # getting fft 
    X = fft(x)

    # get the one side frequency
    n_oneside = N//2
    freq_oneside = freq[:n_oneside]
    X_oneside =X[:n_oneside]
    t_oneside = t[:n_oneside]

    # # plotting freq vs amplitude 
    # plt.figure(figsize = (12, 6))
    # plt.subplot(121)

    # plt.stem(freq_oneside, np.abs(X_oneside), 'g', \
    #         markerfmt=" ", basefmt="-g")
    # plt.xlabel('Freq (Hz)')
    # plt.ylabel('FFT Amplitude |X(freq)|')

    # # plotting inverse
    # plt.subplot(122)
    # plt.plot(t_oneside, ifft(X_oneside), 'ro',markersize=2)
    # plt.xlabel('Time (s)')
    # plt.ylabel('Amplitude')
    # plt.tight_layout()
    # plt.show()

    # # plotting time vs amplitude 
    # plt.figure(figsize=(12,6))
    # plt.plot(t[:n_oneside], np.abs(X[:n_oneside]))
    # plt.xlabel('Period ($seconds$)')
    # plt.ylabel('FFT Amplitude |X(freq)|')

    # plt.show()



    fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.plot(t, x)
    Pxx, freqs, bins, im = ax2.specgram(x,Fs=sr, scale='dB')
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('frequencies (Hz)')
    cbar = plt.colorbar(im, ax=ax2)
    cbar.set_label('Amplitude (dB)')
    cbar.minorticks_on()
    plt.show()


if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n',FILE)
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))

