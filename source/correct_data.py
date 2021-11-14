from pandas import DataFrame
from numpy import mean
import requests
from typing import List, Tuple, Union
import datetime

class MagCorrector:

    def _parse_dates(self, dates: List[str]) -> Tuple:

        dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

        startyear,startmonth,startday = dates[0].split('-')
        endyear,endmonth,endday = dates[-1].split('-')

        return (startyear,startmonth,startday),(startyear,startmonth,startday)


    def _get_value(self, data: DataFrame, dates: List[str], elevation: str) -> Union[int,float]:

        start,end = self._parse_dates(dates)

        lat = mean(data.Lat.values)
        lon = mean(data.Long.values)

        url = ('https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfwmm?model=IGRF&elevationUnits=M&'
        'coordinateSystem=D&lat1=%s&lon1=%s&elevation=%s&startYear=%s&startMonth=%s&startDay=%s&endYear=%s&endMonth=%s'
        '&endDay=%s&resultFormat=json') % (
            lat, lon, elevation, start[0],start[1],start[2],end[0],end[1],end[2])
        print(url)
        r = requests.get(url)
        if r.status_code != 200:
            raise requests.exceptions.RequestException
        
        # print(r.json()['result'][0]['totalintensity'])
        return r.json()['result'][0]['totalintensity']

    def global_detrend(self, data: DataFrame, value: Union[int,float] = None, dates: List[str] = None, elevation: str = None) -> None:
        if not value:
            value = self._get_value(data, dates, elevation)

        data.Mag_nT -= value
