from clients.bart_api_client import bart_api_client
from collections import OrderedDict
from misc import constants
from misc.constants import RESP_HEADER

import json

activities = ['food', 'shopping', 'attraction']


def get_stations():
    return json.dumps({'stations': bart_api_client.get_stations()}), constants.HTTP_STATUS_OK, RESP_HEADER


# Formats platform information for a specific direction from BART API into a much cleaner format
def format_platform_info(station_info, direction):
    platform_info = OrderedDict()
    if '{}_platforms'.format(direction) in station_info and '{}_routes'.format(direction) in station_info:
        platform_info['platforms'] = station_info['{}_platforms'.format(direction)]['platform'] \
            if station_info['{}_platforms'.format(direction)] != '' else []
        platform_info['routes'] = station_info['{}_routes'.format(direction)]['route']

    return platform_info


# Fetches activity information from BART API's station information and formats it a bit more cleanly
def format_activity(station_info, activity):
    activity_info = OrderedDict()
    activity_info['activity_type'] = activity
    activity_info['info'] = station_info[activity]['#cdata-section']
    return activity_info


def format_station_info_resp(station_info):
    formatted_station_info_dict = OrderedDict()
    formatted_station_info_dict['link'] = station_info['link']['#cdata-section']
    formatted_station_info_dict['abbr'] = station_info['abbr']
    formatted_station_info_dict['name'] = station_info['name']
    formatted_station_info_dict['description'] = station_info['intro']['#cdata-section']
    formatted_station_info_dict['lat'] = station_info['gtfs_latitude']
    formatted_station_info_dict['lng'] = station_info['gtfs_longitude']
    formatted_station_info_dict['address'] = station_info['address']
    formatted_station_info_dict['city'] = station_info['city']
    formatted_station_info_dict['state'] = station_info['state']
    formatted_station_info_dict['zipcode'] = station_info['zipcode']
    formatted_station_info_dict['north_info'] = format_platform_info(station_info=station_info, direction='north')
    formatted_station_info_dict['south_info'] = format_platform_info(station_info=station_info, direction='south')
    formatted_station_info_dict['activities'] = [map(lambda a : format_activity(station_info, a), activities)]

    return formatted_station_info_dict


def get_station_info(station_abbr):
    station_info = bart_api_client.get_station_info(station_abbr)
    return json.dumps({'station_info': format_station_info_resp(station_info)}), constants.HTTP_STATUS_OK, \
           RESP_HEADER
