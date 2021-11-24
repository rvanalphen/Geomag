from pandas.core.frame import DataFrame
from pydantic import BaseModel, validator
from pathlib import Path, PosixPath
from typing import List, Optional, Union,Iterable
from pyproj import CRS
from pprint import pprint

class Models(BaseModel):
    line: DataFrame
    shapes: Union[PosixPath,str]
    top_bound: List[Union[int,float]]
    bottom_bound: int
    inclination: int
    declination: int
    intensity: int

    # no current pydantic way to validate dataframe
    class Config:
        arbitrary_types_allowed = True

    @validator('shapes')
    def path_validator(cls, f) -> Path:
        if not f.is_file():
            raise AttributeError(
                'The file specified does not exist; check filepath')
        return f

    @validator('bottom_bound','inclination','declination','intensity',allow_reuse=True)
    def epsg_validator(cls, num) -> int:
        if type(num) != int:
            raise TypeError("Value %i must be an int" % num)
        return num

    @validator('top_bound',each_item=True)
    def top_validator(cls,bnd):
        if type(bnd) != int:
            raise TypeError("Top bounds %i must be an int" % bnd)
        return bnd


class PloufModel(Models):

    @property
    def Parameters(self):
        pprint(self.dict(exclude={'line'},exclude_unset=True))

    def _center_data(self,x0: int, y0: int,offsetX: int = 0,offsetY: int = 0):

        #Centering data around the middle of Survey Line  
        self.line['Northing'] -= x0 - offsetX
        self.line['Easting'] -= y0 - offsetY
        #Centering anomaly around zero
        mag0 =  self.line.Mag_nT.median()
        self.line['Mag_nT'] -= mag0

        return self.line

    def run_model(self):
        x0 = self.line.Northing.median() 
        y0 = self.line.Easting.median()

        self.line = self._center_data(x0,y0)