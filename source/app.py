from pandas.core.frame import DataFrame
from source.clean_data import CleaningStrategy,NorthSouthCleaner,EastWestCleaner
from source.geomag import GeoMag
from source.load_data import path_to_df
from source.correct_data import MagCorrector
from pyproj import Transformer, CRS
from math import atan2, pi

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

class App:
    def __init__(self, parameters: GeoMag) -> None:
        self.parameters = parameters
        self.data: DataFrame = path_to_df(parameters.filepath)

    def transform_coords(self):
        in_crs = CRS.from_epsg(self.parameters.input_epsg)
        out_crs = CRS.from_epsg(self.parameters.output_epsg)

        transformer = Transformer.from_crs(in_crs, out_crs)
        self.data["Easting"], self.data["Northing"] = transformer.transform(
            self.data.Lat.values, self.data.Long.values)

    def _get_heading(self, data: DataFrame) -> None:
        try:
            if 'Easting' in data.columns.values:
                compass = []
                for i in range(len(data.index)-1):
                    pointa = (
                        data.Easting.values[i], data.Northing.values[i])
                    pointb = (
                        data.Easting.values[i+1], data.Northing.values[i+1])
                    compass.append(
                        _direction_lookup(
                            pointb[0], pointa[0], pointb[1], pointa[1])
                    )
                compass.insert(0, 999)

            data["Heading"] = compass

        except:
            raise AttributeError('Data has no Easting or Northing')

    def _choose_strategey(self) -> CleaningStrategy:

        self._get_heading(self.data)

        mode_heading = self.data.Heading.round().mode()[0]

        if mode_heading < 44 or mode_heading > 316\
             or (mode_heading > 136 and mode_heading < 224):
            return NorthSouthCleaner()

        else:
            return EastWestCleaner()

    def clean_data(self):

        cleaning_strategy = self._choose_strategey()
        self.data = cleaning_strategy.cut_heading(self.data)

    def subtract_total_field(self, value: int = None):

        magcorrector = MagCorrector()

        if not value:
            magcorrector.global_detrend(
                self.data, dates=self.parameters.dates, elevation=self.parameters.elevation)
        else:
            magcorrector.global_detrend(self.data, value)
