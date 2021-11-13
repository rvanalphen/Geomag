from pandas import DataFrame
from numpy import mean
import requests
from typing import List, Optional


class MagCorrector:

    def _get_value(self, data: DataFrame, dates: List[str], elevation: str) -> int:

        val_list = []
        lat = mean(data.Lat.values)
        lon = mean(data.Long.values)

        for i, _ in enumerate(dates):

            url = 'https://geomag.bgs.ac.uk/web_service/GMModels/igrf/13/?Latitude=%s&Longitude=%s&altitude=%s&date=%s&format=json' % (
                lat, lon, elevation, dates[i])

            try:
                r = requests.get(url)
                if r.status_code == 200:
                    value = int(r.json()['geomagnetic-field-model-result']
                                ['field-value']['total-intensity']['value'])

                    val_list.append(value)

            except requests.exceptions.RequestException as e: 
                raise SystemExit(e)

        return mean(val_list)

    def global_detrend(self, data: DataFrame, value: int = None, dates: List[str] = None, elevation: str = None) -> None:
        if not value:
            try:
                value = self._get_value(data, dates)
                print("run code ", value)
            except:
                raise AttributeError("Need dates in a list")

        data.Mag_nT -= value
