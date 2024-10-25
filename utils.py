import numpy as np
import xarray as xr
import pandas as pd
from datetime import datetime, timedelta
import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
import matplotlib.ticker as ticker

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import seaborn as sns
import cmocean
import cmocean.cm as cmo

# Data for locations
locations = {
    'BS': {
        'name': 'BS',
        'label': 'Bransf.',
        'order': 0,
        'color': '#d55e00',
        'boxes': [
            {'lonpoly': [302, 300, 300, 298, 298, 300, 300, 302, 302],
             'latpoly': [-62.5,-62.5,-62.6,-62.6,-63.7,-63.7,-63.5,-63.5,-62.5]},
            ]
    },
    'GERL': {
        'name': 'GERL',
        'label': 'Gerl.',
        'order': 1,
        'color': '#029e73',
        'boxes': [
            {'lonpoly': [296.1, 298.5, 299.6, 297.6], 'latpoly': [-64.7, -63.6, -64.0, -65.3]}
        ]
    },
    'GP': {
        'name': 'GP',
        'label': 'Grand.',
        'order': 2,
        'color': '#cc78bc',
        'boxes': [
            {'lonpoly': [291.6, 295.5, 297.6, 294.0], 'latpoly': [-66.7, -64.5, -65.3, -67.4]}
        ]
    },
    'MB2': {
        'name': 'MB',
        'label': 'M. Bay',
        'order': 3,
        'color': '#0173b2',
        'boxes': [
            {'lonpoly': [287.7, 290.5, 294.0, 292.0], 'latpoly': [-69.1, -67.5, -68.5, -69.7]}
        ]
    },
    
    # 'AW': {
    #     'name': 'AW',
    #     'label': 'Amund. West',
    #     'order': 6,
    #     'color': '#c99999',
    #     'boxes': [
    #         {'lonpoly': [240.0, 249.0, 250.0, 239.0], 'latpoly': [-71.0, -71.0, -75.0, -75.0]}
    #     ]
    # },
    
    # 'AE': {
    #     'name': 'AE',
    #     'label': 'Amund. East',
    #     'order': 5,
    #     'color': '#f29143',
    #     'boxes': [
    #         {'lonpoly': [249.0, 260.0, 261.0, 250.0], 'latpoly': [-71.0, -71.0, -75.5, -75.5]}
    #     ]
    # },
    
    # 'BESH': {
    #     'name': 'BEL',
    #     'label': 'Bellingshausen',
    #     'order': 4,
    #     'color': '#f29143',
    #     'boxes': [
    #         {'lonpoly': [272.0, 284.0, 289.0, 275.0], 'latpoly': [-71.5, -70.0, -72.8, -74.5]}
    #     ]
    # },
    
    # 'PBC': {
    #     'name': 'PB',
    #     'label': 'Prydz Bay',
    #     'order': 7,
    #     'color': '#f65e2e',
    #     'boxes': [
    #        {'lonpoly': [70.0, 77.0, 77.0, 70.0], 'latpoly': [-66.0, -66.0, -70.0, -70.0]}
    #     ]
    # },        
}




# Defining the 48.1 polygon with curvature on Side 2 and Side 4, and making sure Sides 5 and 6 are included
lon_side1 = [-70.0, -70.0]  # Side 1: Vertical from 70°W, 70°S to 70°W, 60°S
lat_side1 = [-70.0, -60.0]

lon_side2 = np.linspace(-70.0, -50.0, 100).tolist()  # Side 2: Horizontal from 70°W, 60°S to 50°W, 60°S with curvature
lat_side2 = [-60.0] * 100

lon_side3 = [-50.0, -50.0]  # Side 3: Vertical from 50°W, 60°S to 50°W, 65°S
lat_side3 = [-60.0, -65.0]

# Side 4: Horizontal from 50°W, 65°S to 62°W, 65°S with curvature
lon_side4 = np.linspace(-50.0, -62, 100).tolist()  
lat_side4 = [-65.0] * 100

lon_side5 = [-62, -66]  # Side 5: Diagonal Vertical from [62°W, 65°S] to [66°W, 67°S]
lat_side5 = [-65.0, -67]

lon_side6 = [-66, -66]  # Side 6: Vertical from [66°W, 67°S] to [62°W, 70°S]
lat_side6 = [-67, -70.0]

lon_side7 = [-66, -70.0]  # Side 7: Horizontal from 60°W, 70°S to 70°W, 70°S
lat_side7 = [-70.0, -70.0]

# Concatenate all sides to form the full polygon
lonpoly_48_1 = lon_side1 + lon_side2 + lon_side3 + lon_side4 + lon_side5 + lon_side6 + lon_side7
latpoly_48_1 = lat_side1 + lat_side2 + lat_side3 + lat_side4 + lat_side5 + lat_side6 + lat_side7

# Define Strata
mu_strata = {
    'MU_EI': {
        'name': 'EI',
        'label': 'Elephant Island',
        'order': 0,
        'color': '#d55e00',
        'boxes': [
            {'lonpoly': [-53.4425, -58.0, -58.0, -53.4425], 'latpoly': [-60.0, -60.0, -61.8987, -61.8987]}
        ]
    },
    'MU_SSIW': {
        'name': 'SSIW',
        'label': 'South Shetland Islands West',
        'order': 1,
        'color': '#029e73',
        'boxes': [
            {'lonpoly': [-58.0, -59.4842, -59.5536, -60.5258, -63.3036, -61.9842, -58.0, -58.0],
             'latpoly': [-60.0, -60.0, -60.7958, -60.7958, -62.2125, -62.9563, -61.8987, -60.0]}
        ]
    },
    'MU_BS': {
        'name': 'BS',
        'label': 'Bransfield Strait',
        'order': 2,
        'color': '#cc78bc',
        'boxes': [
            {'lonpoly': [-56.255, -58.0, -61.9842, -59.99497, -56.255], 
             'latpoly': [-61.8987, -61.8987, -62.9563, -63.88167, -63.0083]}
        ]
    },
    'MU_JOIN': {
        'name': 'JOIN',
        'label': 'Joinville Islands',
        'order': 3,
        'color': '#0173b2',
        'boxes': [
            {'lonpoly': [-53.4425, -56.255, -56.255, -53.4425],
             'latpoly': [-61.8987, -61.8987, -63.4167, -63.4167]}
        ]
    },
    'MU_GERL': {
        'name': 'GS',
        'label': 'Gerlache Strait',
        'order': 4,
        'color': '#f0e442',
        'boxes': [
            {'lonpoly': [-62.795, -61.9842, -59.74, -63.5504, -66.3476],
             'latpoly': [-62.5, -62.9563, -64.0, -65.727, -64.3]}
        ]
    },
    '48_1': {
        'name': '48.1',
        'label': 'Antarctic Peninsula',
        'order': 5,
        'color': '#e69f00',
        'boxes': [
        {
            'lonpoly': lonpoly_48_1,
            'latpoly': latpoly_48_1
        }
    ]
    }
}
extents = {
    "base": [275, 311, -72, -59],
    "expand": [274, 316, -71, -60],
    "toSG": [281.6, 322, -65, -60],
    "toAM": [271, 308, -71, -62],
    "hires": [269, 309, -72, -59],
    "bells": [265.54, 305.32, -75.4, -62.8],
    "WAPtoamund": [226.93, 312.34, -76.995, -62.365],
    "prydz": [60.9, 88.2, -74.32000000000001, -58.64],
    "amund": [229.91, 276.58, -76.67, -66.59],

}

# Helper function to plot the base map and all boxes
def plot_region(ax, extent):
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE, zorder=2)
    ax.add_feature(cfeature.LAND, facecolor='silver', zorder=2)
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='black', alpha=0.5, linestyle='--', zorder=1)
    gl.xlocator = ticker.FixedLocator(range(-180, 181, 10))
    gl.ylocator = ticker.FixedLocator(range(-90, 91, 5))
    gl.xlabel_style = {'size': 10, 'color': 'gray'}
    gl.ylabel_style = {'size': 10, 'color': 'gray'}


# Helper function to plot the candidate management units
def plot_mgmt(ax, extent, boxes, box_zorder=6):
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    # Plot all candidate management units
    for region, coords_list in boxes.items():
        for coords in coords_list:
            lonpoly = coords['lonpoly']
            latpoly = coords['latpoly']
            poly = Polygon(list(zip(lonpoly, latpoly)), closed=True, fill=False, alpha=0.25, zorder=box_zorder, transform=ccrs.PlateCarree())
            ax.add_patch(poly)

def plot_nurseries(ax, extent, locations, box_zorder=6, fill=False, color='color', outline='color', alpha=0.25, show_legend=True):
    """
    Plot nurseries with various styles.

    Parameters:
    ax (object): Matplotlib axis object.
    extent (list): The extent of the map [min_lon, max_lon, min_lat, max_lat].
    locations (dict): Dictionary containing location data.
    box_zorder (int): Z-order for the boxes.
    fill (bool): Whether to fill the boxes with color.
    color (str): 'color' to use locations' specific color, 'k' for black fill.
    outline (str): 'color' to use locations' specific color for the outline, 'k' for black outline.
    alpha (float): Transparency level for filled boxes.
    show_legend (bool): Whether to show the legend.
    """
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    
    # Plot all bounding boxes
    for region, loc_data in locations.items():
        for box in loc_data['boxes']:
            lonpoly = box['lonpoly']
            latpoly = box['latpoly']

            # Determine fill color and edge color
            poly_color = loc_data['color'] if color == 'color' else 'k'
            edge_color = loc_data['color'] if outline == 'color' else 'k'

            poly = Polygon(
                list(zip(lonpoly, latpoly)),
                closed=True,
                fill=fill,  # Use the fill parameter
                color=poly_color if fill else 'none',  # Set fill color if fill is True
                edgecolor=edge_color,  # Set edge color based on outline parameter
                alpha=alpha if fill else 1.0,  # Apply transparency only if filling
                zorder=box_zorder,
                transform=ccrs.PlateCarree()
            )
            ax.add_patch(poly)

    # Add legend if show_legend is True
    if show_legend:
        legend_handles = [Line2D([0], [0], color=locations[loc]['color'], lw=2, label=locations[loc]['label']) for loc in locations]
        ax.legend(handles=legend_handles, loc='upper left', title='Nurseries')



# Helper function to plot the base map and all boxes
def plot_nurseries_color(ax, extent, locations, box_zorder=6):
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    # Plot all bounding boxes
    for region, loc_data in locations.items():
        for box in loc_data['boxes']:
            lonpoly = box['lonpoly']
            latpoly = box['latpoly']
            poly = Polygon(list(zip(lonpoly, latpoly)), closed=True, fill=False, edgecolor=loc_data['color'], zorder=box_zorder, transform=ccrs.PlateCarree())
            ax.add_patch(poly)

    # Add legend
    legend_handles = [Line2D([0], [0], color=locations[loc]['color'], lw=2, label=locations[loc]['label']) for loc in locations]
    ax.legend(handles=legend_handles, loc='upper left', title='Nurseries')

def plot_nurseries_colorfill(ax, extent, locations, box_zorder=6, show_legend=True):
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    # Plot all bounding boxes
    for region, loc_data in locations.items():
        for box in loc_data['boxes']:
            lonpoly = box['lonpoly']
            latpoly = box['latpoly']
            poly = Polygon(
                list(zip(lonpoly, latpoly)),
                closed=True,
                fill=True,
                color=loc_data['color'],  # Fill with the specific color
                alpha=0.25,  # Set transparency
                zorder=box_zorder,
                transform=ccrs.PlateCarree()
            )
            ax.add_patch(poly)

    # Add legend if show_legend is True
    if show_legend:
        legend_handles = [Line2D([0], [0], color=locations[loc]['color'], lw=2, label=locations[loc]['label']) for loc in locations]
        ax.legend(handles=legend_handles, loc='upper left', title='Nurseries')


# Helper function to plot the base map and all boxes
def plot_nurseries_bw(ax, extent, locations, box_zorder=6):
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    # Plot all bounding boxes
    for region, loc_data in locations.items():
        for box in loc_data['boxes']:
            lonpoly = box['lonpoly']
            latpoly = box['latpoly']
            poly = Polygon(list(zip(lonpoly, latpoly)), closed=True, fill=False, edgecolor='k', zorder=box_zorder, transform=ccrs.PlateCarree())
            ax.add_patch(poly)

# Helper function to plot the base map and all boxes
def plot_nurseries_bw_fill(ax, extent, locations, box_zorder=6):
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    # Plot all bounding boxes
    for region, loc_data in locations.items():
        for box in loc_data['boxes']:
            lonpoly = box['lonpoly']
            latpoly = box['latpoly']
            poly = Polygon(list(zip(lonpoly, latpoly)), closed=True, fill=True, color ='k', alpha=0.1, zorder=box_zorder, transform=ccrs.PlateCarree())
            ax.add_patch(poly)


# Bring In the Contours:
repo_path = '/Users/zephyrsylvester/repos/hi-res-AP/'
data_path = repo_path + 'data/'
ibsco_path = data_path + 'IBSCO/'

# Path to the downloaded NetCDF file
nc_path = ibsco_path + 'IBCSO_v2_bed_WGS84_500m_APregion.nc'

# Open the NetCDF file using xarray
ds = xr.open_dataset(nc_path)

# Extract the bathymetry data
bathymetry = ds['z']

# Helper function to plot the base map and all boxes
def plot_contour(ax, extent): #  boxes, box_zorder=6
    depth_int = np.arange(-1000, 0, 1000)
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    # Plot the bathymetry contours on the same axis using contour for lines
    contour = ax.contour(bathymetry['lon'], bathymetry['lat'], bathymetry,
                         levels=depth_int, linestyles = 'solid', linewidths=0.5, colors='grey', alpha=0.5,
                         transform=ccrs.PlateCarree(), zorder=0)

    # Add small text in the bottom right corner
    plt.annotate('IBCSO v2 \n 1000m isobath', xy=(1, 0), xycoords='axes fraction',
                 fontsize=6, xytext=(-5, 5), textcoords='offset points', ha='right', va='bottom')



###### OTHER DICTIONS ####

# Data for hypotheses
hypotheses = {
    'h_null': {
        'name': 'h_null',
        'label': 'Ocean',
        'order': 0
    },
    'h_ice': {
        'name': 'h_ice',
        'label': 'Ice',
        'order': 1
    },
    'h_dvm': {
        'name': 'h_dvm',
        'label': 'DVM',
        'order': 2
    },
    'h_size': {
        'name': 'h_size',
        'label': 'Size',
        'order': 3
    }
}


# Data for start years
start_years = {
    2016: {
        'label': 'sy 2016',
        'marker': 'o',  # Circle
        'color': '#648fff'
    },
    2017: {
        'label': 'sy 2017',
        'marker': 's',  # Square
        'color': '#dc267f'
    },
    2018: {
        'label': 'sy 2018',
        'marker': '^',  # Triangle up
        'color': '#ffb000'
    }
}


months_data = {
    1: {
        'label': 'Jan',
        'label_long': 'January',
        'color': '#BBCC33', # Jan - Lime  #month_colors[0],
        'order': 3
    },
    2: {
        'label': 'Feb',
        'label_long': 'February',
        'color': '#EE8866', # Feb - Orange month_colors[1],
        'order': 4
    },
    3: {
        'label': 'Mar',
        'label_long': 'March',
        'color': '#FFAABB', # Mar - pink month_colors[2],
        'order': 5
    },
    4: {
        'label': 'Apr',
        'label_long': 'April',
        'color': '#882255',#'#846551', #EE6677',#,'#AA3377', # Apr - Pink month_colors[3],
        'order': 6
    },
    5: {
        'label': 'May',
        'label_long': 'May',
        'color': '#846551', # May - Purple month_colors[4],882255
        'order': 7
    },
    6: {
        'label': 'Jun',
        'label_long': 'June',
        'color': '#4477AA', # June - Blue month_colors[5],
        'order': 8
    },
    7: {
        'label': 'Jul',
        'label_long': 'July',
        'color': '#bbccee',#'#77AADD', # July - lighter blue month_colors[6],
        'order': 9
    },
    8: {
        'label': 'Aug',
        'label_long': 'August',
        'color': '#BBBBBB', # Aug - Grey, month_colors[7],
        'order': 10
    },
    9: {
        'label': 'Sep',
        'label_long': 'September',
        'color': '#77AADD',#'#bbccee', # Sept - grey month_colors[8],
        'order': 11
    },
    10: {
        'label': 'Oct',
        'label_long': 'October',
        'color': '#66CCEE', # Oct - Cyan, month_colors[9],
        'order': 12
    },
    11: {
        'label': 'Nov',
        'label_long': 'November',
        'color': '#44BB99', # Nov - Teal month_colors[10],
        'order': 1
    },
    12: {
        'label': 'Dec',
        'label_long': 'December',
        'color': '#228833', # Dec - Green month_colors[11],
        'order': 2
    }
}

# # Stage Refernces for coding and plotting
# stages = {
#     0: {
#         'name': 0,
#         'label': 'Embryo',
#         'duration': '0-5d',
#         'color': '#efe7bc',
#         'marker': '.'
#     },
#     1: {
#         'name': 1,
#         'label': 'Nauplii',
#         'duration': '6-22d',
#         'color': '#b4f8c8',
#         'marker': '2'
#     },
#     2: {
#         'name': 2,
#         'label': 'Calyptopes',
#         'duration': '23-60d',
#         'color': '#74bdcb',
#         'marker': '^'
#     },
#     3: {
#         'name': 3,
#         'label': 'Furcilia I-III',
#         'duration': '60-96d',
#         'color': '#3d5b59',
#         'marker': 'o'
#     },
#     4: {
#         'name': 4,
#         'label': 'Furcilia IV+',
#         'duration': '>96d',
#         'color': '#cb5b3b',
#         'marker': 's'
#     }
# }



perry_colors = {'#2892c6', '#6da9b3', '#9fc29a',
                '#cfde81', '#fafa64', '#fcc44d',
                '#fa8c33', '#f25822', '#e70f15' }


from cbmaps import tol_cset

# Load vibrant colors
vibrant_colors = tol_cset('vibrant')

# Updated Stage References for Coding and Plotting
stages = {
    0: {
        'name': 0,
        'label': 'Embryo',
        'duration': '0-5d',
        'color': vibrant_colors.blue,
        'marker': '.'
    },
    1: {
        'name': 1,
        'label': 'Nauplii',
        'duration': '6-22d',
        'color': vibrant_colors.cyan,
        'marker': '2'
    },
    2: {
        'name': 2,
        'label': 'Calyptopes',
        'duration': '23-60d',
        'color': vibrant_colors.teal,
        'marker': '^'
    },
    3: {
        'name': 3,
        'label': 'Furcilia I-III',
        'duration': '60-96d',
        'color': vibrant_colors.orange,
        'marker': 'o'
    },
    4: {
        'name': 4,
        'label': 'Furcilia IV+',
        'duration': '>96d',
        'color': vibrant_colors.magenta,
        'marker': 's'
    }
}
