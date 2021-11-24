
import timeit   
from pathlib import Path
from source.export_data import ExportLines
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.separate_data import SingleSeparator
from source.correct_data import NorthSouthDetrend
from source.model_data import PloufModel

#TODO fix recursive folder creation
######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/cleaned_data/cleaned_lines/'
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
# l5 = pandas.read_csv('./test.in',sep=' ',header=0)

def main():

    print(FILE,'\n')
    # initializing and validating input parameters
    geomag = GeoMag(
        filepath=FILE,
    )

    # creating new App instance with all cleaned data
    app = App(parameters = geomag)
    app.data_is_line()

    
    # DataPlotter().plot_mag_profile(app,'line 1')


    plouf = PloufModel(
        line = app.data,
        shapes= './test.in',
        top_bound= [45],
        bottom_bound= 54,
        inclination= -67,
        declination= 177,
        intensity= 1
    )

    plouf.Parameters







    # app.subtract_mean()

    # # setting up start and endpoints for line extraction 
    # line_params = {
    #     # Line name : [(start coordinates), (end coordinates)]
    #     'line 1': [(534605.4451,4068731.615),(534560.0319,4070426.924)],
    #     'line 2' : [(534678,4068732),(534641,4070410)],
    # }

    # # separating out specific single lines as set in line_params
    # app.separate_lines(SingleSeparator(),line_params)

    # # detrending a line from all lines so it is all about 0
    # key_name='line 1'
    # app.subtract_line(NorthSouthDetrend(),key_name)

    # # creating new instance of data plotter class
    # plotter = DataPlotter()
    # plotter.plot_mag_profile(app,key_name)







if __name__ == "__main__":
    start = timeit.default_timer()
    print('Processing File(s):\n')
    main()
    stop = timeit.default_timer()
    print('\n Data Processed in %f second(s)' % (stop - start))
