from abc import ABC, abstractmethod
from pandas import DataFrame

class CleaningStrategy(ABC):

    @abstractmethod
    def cut_heading(self,data: DataFrame, buffer: int) -> None:
        """[This Abstract Base Class sets a template to take in a pandas DataFrame and optional a buffer. It then only keeps the 
        rows in which they have a heading based on the strategy subclass employed]

        Args:
            data (DataFrame): [DataFrame that is passed into the class containing magnetic survey values]
            buffer (int, optional): [buffer value to make heading cutting less strict]. Defaults to 5.

        Raises:
            AttributeError: [Input is not a DataFrame]
        """

class NorthSouthCleaner(CleaningStrategy):

    def cut_heading(self,data: DataFrame, buffer: int = 5) -> None:

        length = len(data.index)
        cond = []

        for i in range(length):
            if data.Heading[i] < 0+buffer or data.Heading[i] > 360-buffer\
                    or data.Heading[i] > 180-buffer and data.Heading[i] < 180+buffer:

                cond.append(True)
            else:
                cond.append(False)

        return data[cond].reset_index(drop=True)


class EastWestCleaner(CleaningStrategy):

    def cut_heading(self,data: DataFrame, buffer: int = 5) -> None:

        length = len(data.index)
        cond = []

        for i in range(length):
            if data.Heading[i] < 0+buffer or data.Heading[i] > 360-buffer\
                    or data.Heading[i] > 180-buffer and data.Heading[i] < 180+buffer:

                cond.append(True)
            else:
                cond.append(False)

        return data[cond].reset_index(drop=True)









    #         for i in range(length):
    #             if data.Heading[i] < 0+buffer or data.Heading[i] > 360-buffer\
    #                     or data.Heading[i] > 180-buffer and data.Heading[i] < 180+buffer:

    #                 cond.append(True)
    #             else:
    #                 cond.append(False)

    #     elif dir == "EW" or dir == "ew":
    #         for i in range(length):
    #             if data.Heading[i] > 270-buffer and data.Heading[i] < 270+buffer\
    #                     or data.Heading[i] > 90-buffer and data.Heading[i] < 90+buffer:

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

