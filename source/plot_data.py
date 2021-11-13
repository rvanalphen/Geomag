import matplotlib.pyplot as plt
from pandas import DataFrame

class DataPlotter:
    def __init__(self,data: DataFrame) -> None:
        self.data = data
        
    def simple_plot(self,g=None):
        cols = self.data.columns
        fig, ax = plt.subplots(figsize=(10, 10))
        if g == None:
            # giving prioraty to UTM
            if 'Easting' in cols:
                ax.plot(self.data.Easting, self.data.Northing,
                        linestyle='None',marker="o",ms=2)

            else:
                print('convert to utm')
                exit()

            plt.show()
        else:
            ax.plot(self.survey_lines.get_group(g).Easting,
                    self.survey_lines.get_group(g).Northing,
                    linestyle='None',marker="o",ms=2)
            plt.show()

    