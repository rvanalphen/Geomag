from abc import ABC, abstractmethod
from pandas import DataFrame


class DataCleaner(ABC):

    @abstractmethod
    def _direction_lookup(self,destination_x: float, origin_x: float,
         destination_y: float, origin_y: float) -> float:
        """[summary]

        Args:
            destination_x (float): [Latitude of point i+1]
            origin_x (float): [Latitude of point i]
            destination_y (float): [Longitude of point i+1]
            origin_y (float): [Longitude of point i]

        Raises:
            AttributeError: [All inputs must be a float]

        Returns:
            float: [heading calculated between 0 and 360]
        """
    
    @abstractmethod
    def _get_heading(self,data: DataFrame) -> None:
        """[summary]

        Args:
            data (DataFrame): [DataFrame that is passed into the class containing magnetic survey values]

        Raises:
            AttributeError: [Input is not a DataFrame]
        """
    
    @abstractmethod
    def cut_heading(self,data: DataFrame, tolerance: int = 5) -> None:
        """[summary]

        Args:
            data (DataFrame): [DataFrame that is passed into the class containing magnetic survey values]
            tolerance (int, optional): [buffer value to make heading cutting less strict]. Defaults to 5.

        Raises:
            AttributeError: [Input is not a DataFrame]
        """

