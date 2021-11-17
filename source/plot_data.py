import matplotlib.pyplot as plt
from pandas import DataFrame
from typing import Union, Dict
from pathlib import Path

from source.app import App


class DataPlotter:

    def _choose_plot(self, data: DataFrame) -> str:

        mode_heading = data.Heading.round().mode()[0]
        if mode_heading < 44 or mode_heading > 316\
                or (mode_heading > 136 and mode_heading < 224):
            return 'NS'

        return 'EW'

    def simple_plot(self,application: App,lines: bool = False) -> None:
        
        if not application.parameters:
            path = 'Merged Files'
        else:
            path = application.parameters.filepath
            path = str(path).split('/')[-1]
        
        fig, ax = plt.subplots(figsize=(10, 10))

        if not lines:
            data = application.data 
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
            data = application.lines
            for key in data:
                ax.plot(data[key].Easting,data[key].Northing,
                        linestyle='None', marker="o", ms=2)
                
                ax.set_title(path+': all lines')

            plt.show()


    def plot_mag_profile(self,application: App,key_name: str = None,direction: str = None) -> None:

        if not application.parameters:
            path = 'Merged Files'
        else:
            path = application.parameters.filepath
            path = str(path).split('/')[-1]

        data = application.lines[key_name]

        fig, ax = plt.subplots(figsize=(15, 5))

        if key_name:
            ax.set_title(path+': '+key_name)
        else:
            ax.set_title(path+' lines')
        
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


    def plot_offset_profile(self,application: App, offset=150):
    
        data = application.lines

        if not application.parameters:
            path = 'Merged Files'
        else:
            path = application.parameters.filepath
            path = str(path).split('/')[-1]

        start_offset = 0

        fig, ax = plt.subplots(figsize=(10, 10))
        
        for index, (key, value) in enumerate(data.items()):
            if index == 0:
                direction = self._choose_plot(data[key])
            else:
                break

        if "NS" not in direction:
            for key in data:
                ax.plot(data[key].Easting, data[key].Mag_nT+start_offset, marker="o", linestyle='None',
                        markersize=3, label=str(key))

                ax.set_xlabel("Northing")
                ax.set_ylabel("Magnetic Signal (nT)")

                ax.set_title(path+' - Lines offset by: '+str(offset)+'nT')

                ax.legend()
                start_offset += offset
        else:
            for key in data:
                ax.plot(data[key].Northing, data[key].Mag_nT+start_offset, marker="o", linestyle='None',
                        markersize=3, label=str(key))

                ax.set_xlabel("Northing")
                ax.set_ylabel("Magnetic Signal (nT)")

                ax.set_title(path+' - Lines offset by: '+str(offset)+'nT')

                ax.legend()
                start_offset += offset
        plt.show()

