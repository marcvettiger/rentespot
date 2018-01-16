import logging.config

import gmaps

from .core import DataEngine
from .core import Spots

# -*- coding: utf-8 -*-

"""
Spot
~~~~~~~

Spots client library.

"""

__version__ = '0.0.2'
__author__ = 'Marc Vettiger'


logging.config.fileConfig('cfg/logger.conf')
logger = logging.getLogger()


def check_df(s_data_frame):
    #TODO: Check if provided input is of type data frame and from rentepoint (check shape/columns?)
    return True


def get_forecast_days(s_data_frame):
    if check_df(s_data_frame) is False:
        logger.info("Input is no Rentepoint Data Frame")
        return None
    days = s_data_frame.columns[7:].tolist()
    return sorted(days, key=(lambda x : x[-2:]+x[-4:-2]))

def calc_most_stable_spot():
    pass

def get_df_from_GeoLocation_Range():
    pass

def get_creative():
    pass

def print_df_gmap(s_data_frame, day):
    ############################################################
    ### gmap template code
    heat_locations = s_data_frame[['lat', 'lon']]
    weights = s_data_frame[day]

    # heatmap
    spots_heatmap = gmaps.heatmap_layer(heat_locations, weights=weights)
    spots_heatmap.max_intensity = 20
    spots_heatmap.point_radius = 1
    spots_heatmap.dissipating = False

    # get top 10 markers
    #dates = df.columns[7:].tolist()
    #df_top = df.sort_values(dates, ascending=False).head(10)

    top_locations = s_data_frame[['lat', 'lon']]
    info_box_template = """
    <dl>
    <dt>Name</dt><dd>{name}</dd>
    <dt>Country</dt><dd>{country}</dd>
    <dt>Region</dt><dd>{region}</dd>
    <dt>url</dt><dd><a href={url}>{url}</a></dd>
    </dl>
    """.decode('utf-8')
    infobox = s_data_frame[['name', 'country', 'region', 'url']]
    infobox = [info_box_template.format(**info.to_dict()) for _, info in infobox.iterrows()]

    spots_markers = gmaps.marker_layer(top_locations, info_box_content=infobox)
    # show
    fig = gmaps.figure()
    fig.add_layer(spots_heatmap)
    fig.add_layer(spots_markers)
    fig
