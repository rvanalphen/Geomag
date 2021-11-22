from scipy.spatial.distance import cdist
from numpy import linspace
from typing import Union,Dict
from pathlib import PosixPath,Path
import os
from pandas import DataFrame,merge
from functools import reduce



def files_to_dict(dirpath: Union[PosixPath,str]) -> Dict:
    num = 0
    files_dict = {}
    for filename in os.listdir(dirpath):
        if '.' in filename and\
             '20191021_170314.txt' not in filename\
                 and '20191022_003746.txt' not in filename: 
            num += 1
            fullpath = Path(dirpath+filename)
            files_dict[str(num)] = fullpath

    return files_dict

def merge_object_data(dictionary: Dict) -> DataFrame:
    data_list =[]
    for key,value in dictionary.items():
        data_list.append(
            dictionary[key])

    return reduce(lambda left, right: merge(left, right, how='outer'), data_list)


def closest_point(point:list[Union[int,float]], points: list[Union[int,float]]) -> tuple:
    """ Find closest point from a list of points. """
    return points[cdist([point], points).argmin()]

def get_line(data: DataFrame,start: list[Union[int,float]], end: list[Union[int,float]]) -> DataFrame:
    data = data[['Easting','Northing','Mag_nT']]
    df1 = DataFrame()
    df1['point'] = [(x, y) for x,y in zip(data['Easting'],data['Northing'])]
    
    x = linspace(start[0],end[0],endpoint=True,num = 1000)
    y = linspace(start[1],end[1],endpoint=True,num = 1000)

    df2 = DataFrame()
    df2['point'] = [(x, y) for x,y in zip(x, y)]
    
    closest = DataFrame()
    closest['Easting'],closest['Northing'] = list(zip(*[closest_point(x, list(df1['point'])) for x in df2['point']]))
    closest['Mag_nT'] = data['Mag_nT']

    return closest
