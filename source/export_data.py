from datetime import datetime
from typing import Dict,Union
from pathlib import PosixPath
import os
from pandas.core.frame import DataFrame
from abc import ABC, abstractmethod

#TODO finshing making export classes 

class DataExporter(ABC):

    @abstractmethod
    def _make_directory(path: Union[PosixPath, str],lines= False) -> str:
        pass

    @abstractmethod
    def _make_outfile(path: Union[PosixPath, str]) -> str:
        pass 

    @abstractmethod
    def exporter(path: Union[PosixPath, str],data : Union[DataFrame,Dict]) -> None:
        pass




def _make_directory(path: Union[PosixPath, str],lines= False) -> str:
    if type(path) == PosixPath:
        parent_dir = path.parent
    else:
        pass
    
    if not lines:
        outpath = str(parent_dir) + '/' + 'cleaned_data'
    else:
        outpath = str(parent_dir) + '/' + 'cleaned_lines'
    
    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    return outpath

def _make_outfile(path: Union[PosixPath, str]) -> str:
    original_file = os.path.basename(path)
    name,_= original_file.split('.')
    
    date_created = datetime.now().strftime("%Y %m, %d").replace(",","").replace(" ", "_")

    new_file = name+'_processedOn_'+date_created+'.csv'
    
    return new_file
    
def exporter(path: Union[PosixPath, str],data : Union[DataFrame,Dict]) -> None:

    if type(data) == DataFrame:
        outpath = _make_directory(path)
        outfile = _make_outfile(path)
        outpath = outpath+'/'+outfile

        if os.path.isfile(outpath):
            Q = input('Do you want to overwrite %s ? (y/n)' % outfile)
        else:
            Q = 'y'

        if Q =='y':
            data.to_csv(outpath, header=True, index=False)

            print('###')
            print('data output to %s' % outpath)
            print("###")

        else:
            print('###')
            print('data not saved')
            print('###')
            pass

    else:
        for index, (key,value) in enumerate(data.items()):
            outpath = _make_directory(path,lines=True)
            outfile = _make_outfile(path)

            outpath = outpath+'/'+outfile
            one,two = outpath.split('_p')
            outpath = one+'_'+str(key).replace(' ','_')+'_p'+two

            if index ==0 and os.path.isfile(outpath):
                Q = input('Do you want to overwrite all line files ? (y/n)')
            else:
                Q = 'y'

            if Q =='y':
                data[key].to_csv(outpath, header=True, index=False)

                print('###')
                print('data output to %s' % outpath)
                print("###")

            else:
                print('###')
                print('data not saved')
                print('###')
                break