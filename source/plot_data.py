import matplotlib.pyplot as plt
from pandas import DataFrame
from typing import Union, Dict
from pathlib import Path


class DataPlotter:

    def _choose_plot(self, data: DataFrame) -> str:

        mode_heading = data.Heading.round().mode()[0]
        if mode_heading < 44 or mode_heading > 316\
                or (mode_heading > 136 and mode_heading < 224):
            return 'NS'

        return 'EW'

    def simple_plot(self, path: Union[Path, str], data: Union[DataFrame, Dict]) -> None:
        path = str(path).split('/')[-1]
        
        fig, ax = plt.subplots(figsize=(10, 10))

        if type(data) is DataFrame:
            cols = data.columns
            if 'Easting' in cols:
                ax.plot(data.Easting, data.Northing,
                        linestyle='None', marker="o", ms=2)
                ax.set_title(path+': all data')
            else:
                print('convert to utm')
                exit()

            plt.show()

        else:
            for key in data:
                ax.plot(data[key].Easting,data[key].Northing,
                        linestyle='None', marker="o", ms=2)
                
                ax.set_title(path+': all lines')

            plt.show()


    def plot_mag_profile(self, path: Union[Path, str], data: Dict,
                         key_name: str = None, direction: str = None) -> None:

        path = str(path).split('/')[-1]

        if key_name:
            data = data[key_name]

        if type(data) is DataFrame:
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.set_title(path+': '+key_name)

            if not direction:
                direction = self._choose_plot(data)

            if "NS" not in direction:
                ax.plot(data.Easting, data.Mag_nT, marker="o",
                        linestyle='None', markersize=3)

                ax.set_xlabel("Easting")
                ax.set_ylabel("Magnetic Signal (nT)")

                plt.show()

            else:
                ax.plot(data.Northing, data.Mag_nT, marker="o",
                        linestyle='None', markersize=3)

                ax.set_xlabel("Northing")
                ax.set_ylabel("Magnetic Signal (nT)")

                ax.set_title(key_name)

                plt.show()
        else:
            for index, (key, value) in enumerate(data.items()):
                if index == 0:
                    direction = self._choose_plot(data[key])

                self.plot_mag_profile(path, data, key, direction)
