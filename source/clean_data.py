from pandas import DataFrame
from numpy import mean
import math
from source.cleaner import CleaningStrategy

class NorthSouthCleaner(CleaningStrategy):
    def _direction_lookup(self,destination_x: float, origin_x: float,
         destination_y: float, origin_y: float) -> float:
        # CREDIT: https://www.analytics-link.com/post/2018/08/21/calculating-the-compass-direction-between-two-points-in-python
        deltaX = destination_x - origin_x

        deltaY = destination_y - origin_y

        degrees_temp = math.atan2(deltaX, deltaY)/math.pi*180

        if degrees_temp < 0:

            degrees_final = 360 + degrees_temp

        else:

            degrees_final = degrees_temp

        return degrees_final

    
    def _get_heading(self,data: DataFrame) -> None:
        try:
            if 'Easting' in data.columns.values:
                compass = []
                for i in range(len(data.index)-1):
                    pointa = (
                        data.Easting.values[i], data.Northing.values[i])
                    pointb = (
                        data.Easting.values[i+1], data.Northing.values[i+1])
                    compass.append(
                        self._direction_lookup(
                            pointb[0], pointa[0], pointb[1], pointa[1])
                    )
                compass.insert(0, 999)

            data["Heading"] = compass
        

        except:
            raise AttributeError('Data has no Easting or Northing')
    
    def cut_heading(self,data: DataFrame, tolerance: int = 5) -> None:
        if "Heading" not in data.columns:
            self._get_heading(data)

        length = len(data.index)
        cond = []

        for i in range(length):
            if data.Heading[i] < 0+tolerance or data.Heading[i] > 360-tolerance\
                    or data.Heading[i] > 180-tolerance and data.Heading[i] < 180+tolerance:

                cond.append(True)
            else:
                cond.append(False)

        return data[cond].reset_index(drop=True)












    #         for i in range(length):
    #             if data.Heading[i] < 0+tolerance or data.Heading[i] > 360-tolerance\
    #                     or data.Heading[i] > 180-tolerance and data.Heading[i] < 180+tolerance:

    #                 cond.append(True)
    #             else:
    #                 cond.append(False)

    #     elif dir == "EW" or dir == "ew":
    #         for i in range(length):
    #             if data.Heading[i] > 270-tolerance and data.Heading[i] < 270+tolerance\
    #                     or data.Heading[i] > 90-tolerance and data.Heading[i] < 90+tolerance:

    #                 cond.append(True)
    #             else:
    #                 cond.append(False)

    #     else:
    #         print("Must specify a cut by direction either 'NS','EW', or both in a list")
    #         exit()

    #     data = data[cond].reset_index(drop=True)

    # def calc_dist(self,G=False) -> Series:
    #     dist = []
    #     length = len(data.index)
    #     cols = data.columns
    #     data.sort_values(by=['Northing'], ascending=True)
    #     data.reset_index(drop=True)
    #     if 'Easting' in cols:
    #         for i in range(length-1):
    #             pointa = (
    #                 data.Easting.values[i], data.Northing.values[i])
    #             pointb = (
    #                 data.Easting.values[i+1], data.Northing.values[i+1])

    #             dist.append(math.dist(pointa, pointb))
    #     else:
    #         print('need to transform to utm')
    #         exit()

    #     dist.insert(0, 0)

    #     data["Dist"] = dist

