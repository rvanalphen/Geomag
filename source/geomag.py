from pydantic import BaseModel, validator
from pathlib import Path
from typing import List, Optional
from pyproj import CRS
import string

class GeoMag(BaseModel):

    filepath: Path or string
    input_epsg: Optional[str] = None
    output_epsg: Optional[str] = None
    dates: Optional[List[str]] = None
    elevation: Optional[str] = '0'

    @validator('filepath',pre=True,check_fields=True)
    def path_validator(cls, f) -> Path:
        if not f.is_file():
            raise AttributeError(
                'The file specified does not exist; check filepath')
        return f

    @validator('input_epsg','output_epsg',allow_reuse=True)
    def epsg_validator(cls, code) -> str:
        if not code.isdigit():
            raise ValueError(
                "EPSG: code must be a string of all numbers, example: '4326' ")
        
        return code

    @validator('dates')
    def dates_validator(cls,dts):
        if not type(dts) == List:
            raise TypeError('Dates must be of type List')
                
        return dts

    @validator('elevation',allow_reuse=True)
    def epsg_validator(cls, elev) -> str:
        if not elev.isdigit():
            raise ValueError(
                "Elevation must be a digit of type str")
        
        return elev  
