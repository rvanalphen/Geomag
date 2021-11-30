from typing import Dict, List
from pandas.core.frame import DataFrame
from source.cut_data import CuttingStrategey, NorthSouthCut, EastWestCut
from source.geomag import GeoMag
from source.load_data import path_to_df
from source.correct_data import MagCorrector
from pyproj import Transformer, CRS
from math import atan2, pi
from source.separate_data import DataSeparator
from source.export_data import DataExporter
from source.correct_data import MagDetrender
from pprint import pprint

def _direction_lookup(destination_x: float, origin_x: float,
                      destination_y: float, origin_y: float) -> float:
    # CREDIT: https://www.analytics-link.com/post/2018/08/21/calculating-the-compass-direction-between-two-points-in-python
    deltaX = destination_x - origin_x

    deltaY = destination_y - origin_y

    degrees_temp = atan2(deltaX, deltaY)/pi*180

    if degrees_temp < 0:

        degrees_final = 360 + degrees_temp

    else:

        degrees_final = degrees_temp

    return degrees_final

class MagApp:
    def __init__(self, parameters: GeoMag = None,merged_patches: DataFrame = None) -> None:

        if parameters != None and merged_patches is None:
            self.parameters = parameters
            self.data: DataFrame = path_to_df(parameters.filepath)
            self.lines: Dict = None

        else:
            self.parameters = parameters
            self.data: DataFrame = merged_patches
            self.lines: Dict = None

    @property
    def Data(self):
        print(self.data)
    
    @property
    def Lines(self):
        print(self.lines)
    
    @property
    def Parameters(self):
        print_dict={}
        for p in self.parameters:
           print_dict[p[0]] = p[1]
        
        pprint(print_dict)

    @property
    def Attributes(self):
        print("App Parameters:")
        self.Parameters
        print("\n")
        print("File Data:")
        self.Data
        print("\n")
        print("Data Separated into Lines")
        self.Lines

    def _set_lines(self,data: DataFrame, key_name: str) -> None:
        if not self.lines:
            self.lines = {}
        self.lines[key_name] = data

    def data_is_line(self):
        self._set_lines(self.data,'line 1')

    def transform_coords(self) -> List:
        in_crs = CRS.from_epsg(self.parameters.input_epsg)
        out_crs = CRS.from_epsg(self.parameters.output_epsg)

        transformer = Transformer.from_crs(in_crs, out_crs)
        self.data["Easting"], self.data["Northing"] = transformer.transform(
            self.data.Lat.values, self.data.Long.values)

    def _get_heading(self) -> None:
        cols = self.data.columns.values
        if 'Easting' in cols:
            compass = []
            for i in range(len(self.data.index)-1):
                pointa = (
                    self.data.Easting.values[i],self.data.Northing.values[i])
                pointb = (
                    self.data.Easting.values[i+1],self.data.Northing.values[i+1])
                compass.append(
                    _direction_lookup(
                        pointb[0], pointa[0], pointb[1], pointa[1])
                )
            compass.insert(0, 999)

        self.data["Heading"] = compass

    def _choose_strategey(self) -> CuttingStrategey:

        self._get_heading()

        mode_heading = self.data.Heading.round().mode()[0]

        if mode_heading < 44 or mode_heading > 316\
                or (mode_heading > 136 and mode_heading < 224):
            self.data['Dir'] = 'NS'   
            return NorthSouthCut()

        else:
            self.data['Dir'] = 'EW'   
            return EastWestCut()

    def cut_data(self,buffer: int = 5) -> None:

        cleaning_strategy = self._choose_strategey()
        self.data = cleaning_strategy.cut_heading(self.data,buffer)


    def subtract_total_field(self, value: int = None) -> None:

        if not value:
            MagCorrector().global_detrend(
                self.data, dates=self.parameters.dates, elevation=self.parameters.elevation)
        else:
            MagCorrector().global_detrend(self.data, value)

    def subtract_mean(self):
        MagCorrector().minus_mean(self.data)

    def subtract_line(self,detrend_strategy: MagDetrender, key_name: str = None):
        if not key_name:
            for key in self.lines.keys():
                self.lines[key] = detrend_strategy.detrend(self.lines[key])
        else:
            self.lines[key_name] = detrend_strategy.detrend(self.lines[key_name])

    def _update_data(self) -> None:
        # Q = input('Do you want to only keep patch data that match those seperated into single lines? (y/n)')
        Q='y'
        if Q == 'y':
            idx =[]
            for key in self.lines:
                idx.extend(self.lines[key].index.values)
        
            self.data = self.data[self.data.index.isin(idx)]
            print('Patch data was updated')
        
        else:
            print('Patch data was not updated')

    def separate_lines(self, separation_strategy: DataSeparator,line_params: Dict = None, buffer: int = 10) -> Dict:
        if not line_params:
            self.lines = separation_strategy.split(self.data)
            self._update_data()
        else:
            self.lines = separation_strategy.split(self.data,line_params,buffer)
            del self.data['geometry']

    def export_data(self,export_strategy: DataExporter,override_name: str = None):
        export_strategy.exporter(self.parameters.filepath,self.data,self.lines,override_name)


        