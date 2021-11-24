import string
from typing import Tuple
from pandas import DataFrame,read_csv

def _parse_file(filepath: string) -> Tuple:
    import csv
    try:
        with open(filepath, 'r') as tmp:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(tmp.read(4024))  #### detect delimiters
            head = sniffer.has_header(tmp.read(4024))  #### detect header 
            tmp.seek(0)
            if not head:
                head = 'None'
            head = 0
        return (dialect.delimiter,head)
    except csv.Error:
        with open(filepath, 'r') as tmp:
            sniffer = csv.Sniffer()
            head = sniffer.has_header(tmp.read(4024))  #### detect header 
            tmp.seek(0)
            if not head:
                head = 'None'
            head = 0
        return (' ',head)

def path_to_df(filepath: string) -> DataFrame:
    params = _parse_file(filepath)
    return read_csv(filepath,sep=params[0],header=params[1])