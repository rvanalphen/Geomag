from pandas.core.frame import DataFrame
from source.cleaner import CleaningStrategy
from source.geomag import GeoMag
from source.load_data import path_to_df
from source.correct_data import MagCorrector
from pyproj import Transformer
from typing import Optional

class App:
    def __init__(self, parameters: GeoMag) -> None:
        self.parameters = parameters 
        self.data: DataFrame = path_to_df(parameters.filepath)

    def transform_coords(self):
        transformer = Transformer.from_crs(self.parameters.input_epsg,self.parameters.output_epsg)
        self.data["Easting"],self.data["Northing"] = transformer.transform(self.data.Lat.values,self.data.Long.values)

    def clean_data(self,cleaning_strategy: CleaningStrategy):
        self.data = cleaning_strategy.cut_heading(self.data)

    def subtract_total_field(self,value: int = None):
        magcorrector = MagCorrector()
        if not value:
            magcorrector.global_detrend(self.data,self.parameters.date_range)
        else:
            magcorrector.global_detrend(self.data,value)
