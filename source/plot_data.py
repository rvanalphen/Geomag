import matplotlib.pyplot as plt
import subprocess
import pygmt as gmt
import os
from pandas import DataFrame
from source.app import App
from source.model_data import PloufModel



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


    def plot_offset_profile(self,application: App, offset=150) -> None:
    
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

    def plot_model(self,observed: App, model: PloufModel,key_name='line 1') -> None:
        observed = observed.lines[key_name]

        fig, ax = plt.subplots(figsize=(10, 10))

        ax.plot(observed.Northing,observed.Mag_nT,'go',ms=2,label='Observed')

        for key in model.results.keys():
            ax.plot(model.results[key].dist,model.results[key].mag,'r-',ms=2,label='Calculated')

        ax.set_xlabel('Horizontal distance north from line center')
        ax.set_ylabel('Magnetic Anomaly (nT)')
        ax.legend(loc='lower left')
        plt.show()


    def _Createcpt(self,color,scale=None):

        netcdf = "./grid.nc"

        if scale:
            cptSeries=scale+'/1'
        else:
            cptSeries = subprocess.run(
                ['gmt', 'grdinfo', '-T-', netcdf], capture_output=True, text=True)


            
            cptSeries = cptSeries.stdout[2:]
            cptSeries = cptSeries+'/1'

        gmt.makecpt(cmap=color, series=cptSeries,
                    continuous=True, verbose='w', output='geomag.cpt')

    def _GMTcreatNetCDF(self, df, spacing,skip=False):
        print('###')
        if skip:
            Q = 'n'
        else:
            Q = input(
                'do you want to input your own bounds? Otherwise it will be calcuLated for you.(y/n) ')
            bounds = ''

        cols = df.columns
        # giving prioraty to UTM
        if 'Easting' in cols:
            table = df[['Easting', 'Northing', "Mag_nT"]]

            if Q != 'y':
                bounds = str(df.Easting.min())+'/'+str(df.Easting.max()) + '/' + \
                    str(df.Northing.min())+'/' + \
                    str(df.Northing.max())

            else:
                bnds = input('input bounds without -R ')
                bounds = str(bnds)

        else:
            print('Data needs to be transformed into a utm coordinate system')
            exit()

        gmt.blockmedian(table, spacing=spacing, region=bounds,
                        verbose='w', outfile='./blkmdn.gmt')

        gmt.surface(data='./blkmdn.gmt', spacing=spacing, region=bounds,
                    verbose='w', outfile='./grid.nc')

    def GMTHeatmap(self,df, outfile, spacing,colorscale='haxby',scale=None,skip=False):
            netcdf = "./grid.nc"
            cmap = "./geomag.cpt"
            bkmdn = './blkmdn.gmt'

            f1 = os.path.isfile(outfile)
            f2 = os.path.isfile(bkmdn)
            f3 = os.path.isfile(netcdf)
            f4 = os.path.isfile(cmap)
            if f1:
                subprocess.run(["rm",outfile])
            if f2:
                subprocess.run(["rm",bkmdn])
            if f3:
                subprocess.run(["rm",netcdf])
            if f4:
                subprocess.run(["rm",cmap])


            self._GMTcreatNetCDF(df,spacing,skip)
            self._Createcpt(colorscale,scale)


            grdBounds = subprocess.run(
                ['gmt', 'grdinfo', '-I-', netcdf], capture_output=True, text=True)
            grdBounds = grdBounds.stdout[2:]

            fig = gmt.Figure()
            gmt.config(MAP_FRAME_TYPE="plain")
            gmt.config(FORMAT_GEO_MAP="ddd.xx")

            fig.basemap(projection='x1:10000', region=grdBounds,
                        frame=['af', 'WeSn'],  verbose='w')

            fig.grdimage(grid=netcdf, cmap=cmap,
                        frame='+t"Survey Heatmap"', verbose='w')

            fig.colorbar(cmap=cmap,
                        frame='af', position='JMR', verbose='w')

            if skip:
                pass
            else:
                print('###')
                Q = input('do you want to contour your map?.(y/n) ')
                if Q == 'y':
                    interval = input(
                        'What contour interval do you want? annotations will be 2 times your inteval ')
                    contour = str(interval)
                    anno = int(contour)*2
                    anno = str(anno)
                    fig.grdcontour(grid=netcdf, interval=contour,
                                annotation=anno, pen='0.5p', verbose='w')
                else:
                    pass
            
            subprocess.run(['rm', './grid.nc', './blkmdn.gmt', './geomag.cpt'])
            print('saving figure')
            fig.savefig(outfile)