#%%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.img_tiles import GoogleTiles
import matplotlib.patches as mpatches
import pandas as pd
from math import floor
import geopandas as gpd
from matplotlib import patheffects
from source.app import App

def _utm_from_lon(lon):
    """
    _utm_from_lon - UTM zone for a longitude

    Not right for some polar regions (Norway, Svalbard, Antartica)

    :param float lon: longitude
    :return: UTM zone number
    :rtype: int
    """
    return floor((lon + 180) / 6) + 1


def _make_segments(xy,segments,length):
    # written by me (Robert Van Alphen)
    all_segments=[]
    colors=[]
    for index in range(segments):
        if index %2== 0:
            colors.append('black')
        else:
            colors.append('white')

        if index==0:
            s1 = [xy[0],xy[1]-((length/segments)*(segments-1))]

        elif index > 0 and index < segments-1:  
            smid = [xy[1]-((length/segments)*(index+1)),xy[1]-((length/segments)*index)]
            all_segments.append(smid)
        else:
            snth = [xy[1]-((length/segments)),xy[1]]

    all_segments.reverse()
    all_segments.insert(0, s1)
    all_segments.insert(len(all_segments), snth)

    for index,seg in enumerate(all_segments):
        if index %2== 0:
            colors.append('black')
        else:
            colors.append('white')

    return all_segments,colors
    
def _get_segment_nums(length,segments,units):
    # written by me (Robert Van Alphen)
    seg_nums=[]
    for i in range(segments):
        if i !=0:
            seg_nums.append(
                str(round((length/segments)*i)))

    if units == 'km':
        for i in range(len(seg_nums)):
            seg_nums[i] = str(round(int(seg_nums[i])/1000))

    if units == 'km':
        seg_nums.insert(len(seg_nums),str(int(length)/1000) + ' ' + units)
    else:
        seg_nums.insert(len(seg_nums),str(length) + ' ' + units)

    seg_nums.insert(0,'0')
    return seg_nums

def _scale_bar(ax, proj, length,segments=4, location=(0.5, 0.05), linewidth=5,
              m_per_unit=1, units='m'):
    """

    http://stackoverflow.com/a/35705477/1072212
    ax is the axes to draw the scalebar on.
    proj is the projection the axes are in
    location is center of the scalebar in axis coordinates ie. 0.5 is the middle of the plot
    length is the length of the scalebar in km.
    linewidth is the thickness of the scalebar.
    units is the name of the unit
    m_per_unit is the number of meters in a unit
    """

    # find lat/lon center to find best UTM zone
    x0, x1, y0, y1 = ax.get_extent(proj.as_geodetic())
    # Projection in metres
    utm = ccrs.UTM(_utm_from_lon((x0+x1)/2))
    # Get the extent of the plotted area in coordinates in metres
    x0, x1, y0, y1 = ax.get_extent(utm)
    # Turn the specified scalebar location into coordinates in metres
    sbcx, sbcy = x0 + (x1 - x0) * location[0], y0 + (y1 - y0) * location[1]
    # Generate the x coordinate for the ends of the scalebar
    bar_xs = [(sbcx - length * m_per_unit/2), sbcx + length * m_per_unit/2]
    # buffer for scalebar
    buffer = [patheffects.withStroke(linewidth=7, foreground="w")]
    buffer2 = [patheffects.withStroke(linewidth=3, foreground="w")]

    # Plot the scalebar
    # written by me (Robert Van Alphen)
    all_segments,colors = _make_segments(bar_xs,segments,length)    
    seg_nums = _get_segment_nums(length,segments,units)
    for i in range(len(all_segments)):
        ax.plot(all_segments[i], [sbcy, sbcy], transform=utm, color=colors[i],
            linewidth=linewidth, path_effects=buffer)

        ax.text(all_segments[i][0], sbcy+(linewidth+(linewidth/2)),seg_nums[i],
            transform=utm,horizontalalignment='center',
            verticalalignment='bottom',path_effects=buffer2)


    # buffer for text
    buffer = [patheffects.withStroke(linewidth=3, foreground="w")]

    # Plot the scalebar label
    # written by me (Robert Van Alphen)
    end_coords=all_segments[-1][0]+(all_segments[-1][1]-all_segments[-1][0])#+500000

    if units =='km':
        end_num  = str(round(int(length)/1000))
    else:
        end_num = str(length)

    ax.text(end_coords-3, sbcy+(linewidth+(linewidth/2)),
        end_num + ' ' + units, transform=utm,
        horizontalalignment='center', verticalalignment='bottom',
        path_effects=buffer, zorder=2)

    # Plot the N arrow
    ax.text(end_coords-(length+(length/4)), (sbcy-linewidth)+2, u'\u25B2\nN', transform=utm,
        horizontalalignment='center', verticalalignment='bottom',
        path_effects=buffer, zorder=5)



def _get_zoom(ax, crs):
    x0, x1, _, _ = ax.get_extent(crs.as_geodetic())
    # Projection in metres
    utm = ccrs.UTM(_utm_from_lon((x0+x1)/2))
    # Get the extent of the plotted area in coordinates in metres
    x0, x1, _, _ = ax.get_extent(utm)

    diff = x1 - x0
    if diff > 300 and diff < 500:
        zoom = 10
    elif diff > 500 and diff < 2000:
        zoom = 15
    else:
        zoom = 20

    return zoom

def _plot_legend(ax, lcolors, label, location=(0.25, 0.05)):
    labels=[]
    labels.append(label)

    legend_list = []
    for color in lcolors:
        legend_list.append(
            mpatches.Rectangle((0, 0), 1, 1, facecolor=color))

    ax.legend(legend_list, labels,
              loc='lower left', bbox_to_anchor=location, fancybox=True)


def _cartopy_main(app: App,transform, length=100, segments=5,unit='m'):
        tiler = GoogleTiles(style='satellite')

        ext = (app.data.Long.min(),
                app.data.Long.max(),
                app.data.Lat.min(),
                app.data.Lat.max())
        
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(1, 1, 1, projection=tiler.crs)
        ax1.set_extent(ext)
        ax1.add_image(tiler, _get_zoom(ax1,tiler.crs))
        

        gl = ax1.gridlines(draw_labels=True)
        gl.top_labels = False
        gl.right_labels = False
        
        plt.tight_layout()

        return ax1

def cartoplot(app: App,data_name: str,length=100, segments=5,unit='m'):
    
    transform = ccrs.PlateCarree()
    color = ['blue']

    carto_ax = _cartopy_main(app,transform,length,segments,unit)

    carto_ax.scatter(app.data["Long"],app.data["Lat"],color=color,s=1,transform=transform)
    
    _scale_bar(carto_ax, transform,length=length, segments=segments,location=(0.65, 0.025),units=unit)

    _plot_legend(carto_ax,color,data_name,location=(0.1, 0.025))

    plt.show()


