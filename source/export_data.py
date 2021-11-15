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
    def exporter(path: Union[PosixPath, str],data : DataFrame, lines: Dict) -> None:
        pass


class ExportPatch(DataExporter):

    def _make_directory(self,path: Union[PosixPath, str]) -> str:
        if type(path) == PosixPath:
            parent_dir = path.parent
        else:
            #TODO fill in for string
            pass
        
        outpath = str(parent_dir) + '/' + 'cleaned_data'

        
        if not os.path.isdir(outpath):
            os.mkdir(outpath)

        return outpath

    
    def _make_outfile(self,path: Union[PosixPath, str]) -> str:

        original_file = os.path.basename(path)
        name,_= original_file.split('.')
        
        date_created = datetime.now().strftime("%Y %m, %d").replace(",","").replace(" ", "_")

        new_file = name+'_processedOn_'+date_created+'.csv'
        
        return new_file

    def exporter(self,path: Union[PosixPath, str],data : DataFrame, lines: Dict) -> None:
        outpath = self._make_directory(path)
        outfile = self._make_outfile(path)
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

class ExportLines(DataExporter):

    def _make_directory(self,path: Union[PosixPath, str]) -> str:
        if type(path) == PosixPath:
            parent_dir = path.parent
        else:
            #TODO fill in for string
            pass
        
        outpath = str(parent_dir) + '/' + 'cleaned_lines'

        
        if not os.path.isdir(outpath):
            os.mkdir(outpath)

        return outpath

    def _make_outfile(self,path: Union[PosixPath, str],key: str) -> str:

        original_file = os.path.basename(path)
        name,_= original_file.split('.')
        
        date_created = datetime.now().strftime("%Y %m, %d").replace(",","").replace(" ", "_")

        new_file = name+'_'+str(key)+'_processedOn_'+date_created+'.csv'
        
        return new_file

    def exporter(self,path: Union[PosixPath, str],data : DataFrame, lines: Dict) -> None:
        for index, (key,value) in enumerate(lines.items()):
            outpath = self._make_directory(path)
            outfile = self._make_outfile(path,key)

            outpath = outpath+'/'+outfile

            if index ==0 and os.path.isfile(outpath):
                Q = input('Do you want to overwrite all line files ? (y/n)')
            else:
                Q = 'y'

            if Q =='y':
                lines[key].to_csv(outpath, header=True, index=False)

                print('###')
                print('data output to %s' % outpath)
                print("###")

            else:
                print('###')
                print('data not saved')
                print('###')
                break