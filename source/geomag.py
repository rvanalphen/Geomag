from pydantic import BaseModel, validator
from pathlib import Path
from typing import List, Optional
from pyproj import CRS
import string

class GeoMag(BaseModel):

    filepath: Path or string
    direction: Optional[str] = 'NS'
    input_epsg: Optional[str] = None
    output_epsg: Optional[str] = None
    date_range: Optional[List[str]] = None

    @validator('filepath',pre=True,always=True)
    def path_validator(cls, f) -> Path:
        if not f.is_file():
            raise AttributeError(
                'The file specified does not exist; check filepath')
        
        return f

    @validator('direction')
    def direction_validatior(cls, d) -> str:
        if 'ns' or 'ew' not in d:
            raise ValueError("Direction must be a string of 'NS' or 'EW'")

        if d.islower():
            return d.upper()

        return d

    @validator('input_epsg','output_epsg')
    def epsg_validator(cls, code) -> str:
        if not code.isdigit():
            raise ValueError(
                "EPSG: code must be a string of all numbers, example: '4326' ")
        
        return CRS.from_epsg(code)