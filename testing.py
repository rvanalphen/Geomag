
import timeit   
from pathlib import Path, PosixPath
from typing import Dict, Union
import pandas

from pandas.core.frame import DataFrame
from source.plot_data import DataPlotter
from source.geomag import GeoMag
from source.app import App
from source.seperate_data import DistanceSperator, HistSeperator
from source.export_data import ExportPatch,ExportLines,ExportAll
from source.cut_data import NorthSouthCut,EastWestCut
import os
from pandas import merge
from functools import reduce

#TODO fix recursive folder creation
######################## - INPUTS - #############################

DATA_DIR = '/home/robert/DataStorage/Amargosa/rawdata/patches/cleaned_data'
FILE = Path(f'{DATA_DIR}/All_NS_processedOn_2021_11_17.csv')# north - south lines

import matplotlib.pyplot as plt
from math import sqrt
df = pandas.read_csv(FILE,sep=',')

bins = 55
cut_df = pandas.cut(df['Easting'],bins)
# print(pandas.cut(df['Easting'],bins).value_counts())
print(cut_df)
