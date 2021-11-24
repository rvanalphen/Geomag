from pandas.core.frame import DataFrame
from pydantic import BaseModel, validator
from pathlib import Path, Path
from typing import Dict, List, Optional, Union,Iterable
from pyproj import CRS
from pprint import pprint

from source.load_data import path_to_df

class Models(BaseModel):
    line: DataFrame
    shapes: List[Union[Path,str]]
    top_bound: List[Union[int,float]]
    bottom_bound: int
    inclination: int
    declination: int
    intensity: int
    shape_dict: Dict = None

    # no current pydantic way to validate dataframe
    class Config:
        arbitrary_types_allowed = True

    @validator('shapes',each_item=True)
    def path_validator(cls, f) -> Path:
        if not f.is_file():
            raise AttributeError(
                'The file specified does not exist; check filepath')
        return f

    @validator('top_bound',each_item=True)
    def top_validator(cls,bnd):
        if type(bnd) != int:
            raise TypeError("Top bounds %i must be an int" % bnd)
        return bnd

    @validator('bottom_bound','inclination','declination','intensity',allow_reuse=True)
    def other_validator(cls, num) -> int:
        if type(num) != int:
            raise TypeError("Value %i must be an int" % num)
        return num

class PloufModel(Models):

    @property
    def Parameters(self):
        pprint(self.dict(exclude={'line'},exclude_unset=True))
    
    def _shapes_path_to_list(self):
        shape_d = {}
        for i,shape in enumerate(self.shapes):
            name = 'shape %i' % (i+1)
            shape_d[name] = path_to_df(shape)

        self.shape_dict = shape_d

    def _center_line(self,x0: int, y0: int):

        #Centering data around the middle of Survey Line  
        self.line['Northing'] -= x0
        self.line['Easting'] -= y0
        #Centering anomaly around zero
        mag0 =  self.line.Mag_nT.mean()
        self.line['Mag_nT'] -= mag0

        return self.line

    def _center_shapes(self,x0: int, y0: int):

        for key in self.shape_dict.keys():
            self.shape_dict[key]['Northing'] -= x0
            self.shape_dict[key]['Easting'] -= y0
            print(
            self.shape_dict[key]['Easting']
            )
        return self.shape_dict

    def run_model(self):
        self._shapes_path_to_list()

        x0 = self.line.Northing.mean() 
        y0 = self.line.Easting.mean()

        self.line = self._center_line(x0,y0)
        self.shape_dict = self._center_shapes(x0,y0)

