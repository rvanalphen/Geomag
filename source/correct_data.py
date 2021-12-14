from abc import ABC, abstractmethod
from pandas import DataFrame
from numpy import mean
import requests
from typing import List, Tuple, Union
import datetime

class MagCorrector:

    def _parse_dates(self, dates: List[str]) -> Tuple:
        
        if len(dates) > 1:
            dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
        
            startyear,startmonth,startday = dates[0].split('-')
            endyear,endmonth,endday = dates[-1].split('-')
       
        else:
            startyear,startmonth,startday = dates[0].split('-')
            endyear,endmonth,endday = dates[0].split('-')

        return (startyear,startmonth,startday),(endyear,endmonth,endday)


    def _get_value(self, data: DataFrame, dates: List[str], elevation: str) -> Union[float,int]:

        start,end = self._parse_dates(dates)

        lat = mean(data.Lat.values)
        lon = mean(data.Long.values)

        url = ('https://www.ngdc.noaa.gov/geomag-web/calculators/calculateIgrfwmm?model=IGRF&elevationUnits=M&'
        'coordinateSystem=D&lat1=%s&lon1=%s&elevation=%s&startYear=%s&startMonth=%s&startDay=%s&endYear=%s&endMonth=%s'
        '&endDay=%s&resultFormat=json') % (
            lat, lon, elevation, start[0],start[1],start[2],end[0],end[1],end[2])

        # print(url)
        r = requests.get(url)
        if r.status_code != 200:
            raise requests.exceptions.RequestException
        
        # print(r.json()['result'][0]['totalintensity'])
        return r.json()['result'][0]['totalintensity']

    def global_detrend(self, data: DataFrame, value: Union[float,int] = None, dates: List[str] = None, elevation: str = None) -> None:
        if not value:
            value = self._get_value(data, dates, elevation)

        data.Mag_nT -= value


    def minus_mean(self,data: DataFrame):
        data.Mag_nT -=  data['Mag_nT'].mean()

class MagDetrender(ABC):

    @abstractmethod
    def _make_detrend_line(self):
        pass

    @abstractmethod
    def detrend(self):
        pass

class NorthSouthDetrend(MagDetrender):

    def _make_detrend_line(self,data: DataFrame):
        X1, Y1 = data.Northing.min(), data.Mag_nT.iloc[0]
        X2, Y2 = data.Northing.max(), data.Mag_nT.iloc[-1]
        dy = (Y2-Y1)
        dx = (X2-X1)
        m = (dy/dx)
        b = Y1 - (m*X1)

        correction_line = []
        for i,_ in enumerate(data.index):
            mx = data.Northing.values[i] *m
            y = mx +b 
            correction_line.append(y)

        return correction_line

    def detrend(self, data: DataFrame):

        data = data.sort_values(by=['Northing'], ascending=True).reset_index(drop=True)
        
        correction_line = self._make_detrend_line(data)
        
        detrend_mag =[]
        for i,_ in enumerate(data.index):
            detrend_mag.append(
                data.Mag_nT.values[i]-correction_line[i]
            )

        data['Mag_nT'] = detrend_mag

        return data

class EastWestDetrend(MagDetrender):

    def _make_detrend_line(self,data: DataFrame):
        X1, Y1 = data.Easting.min(),data.Mag_nT.iloc[0]
        X2, Y2 = data.Easting.max(),data.Mag_nT.iloc[-1]
        dy = (Y2-Y1)
        dx = (X2-X1)
        m = (dy/dx)
        b = Y1 - (m*X1)

        correction_line = []
        for i,_ in enumerate(data.index):
            mx = data.Easting.values[i] *m
            y = mx +b 
            correction_line.append(y)

        return correction_line

    def detrend(self, data: DataFrame):

        data = data.sort_values(by=['Easting'], ascending=True).reset_index(drop=True)
        
        correction_line = self._make_detrend_line(data)
        
        detrend_mag =[]
        for i,_ in enumerate(data.index):
            detrend_mag.append(
                data.Mag_nT.values[i]-correction_line[i]
            )

        data['Mag_nT'] = detrend_mag

        return data