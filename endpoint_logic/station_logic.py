from collections import OrderedDict
from misc import constants
from misc.constants import RESP_HEADER

import json
import requests
import xmltodict


def get_stations(bart_api_key):
    stations_resp = requests.get(constants.STATIONS_ENDPOINT.format(bart_api_key))
    # NOTE: Bart API apparently returns 200 for literally every case ever. So, we need to check what's the appropriate
    # course of action by checking to see if it's a XML response or a JSON response
    if stations_resp.status_code == constants.HTTP_STATUS_OK:
        try:
            resp = xmltodict.parse(stations_resp.content)
            return json.dumps({'message': resp['root']['message']['error']['details']}), constants.HTTP_BAD_REQUEST, \
                   RESP_HEADER
        except Exception:
            return json.dumps({'stations': json.loads(stations_resp.content)['root']['stations']['station']}), \
                   RESP_HEADER
    else:
        return json.dumps({'message': constants.TRY_AGAIN_LATER}), stations_resp.status_code, RESP_HEADER


def to_ordered_station_info_dict(station_info=None):
    if station_info is None:
        return

    ordered_dict = OrderedDict()
    ordered_dict['link'] = station_info['link']
    ordered_dict['abbr'] = station_info['abbr']
    ordered_dict['name'] = station_info['name']
    ordered_dict['description'] = station_info['description']
    ordered_dict['lat'] = station_info['lat']
    ordered_dict['lng'] = station_info['lng']
    ordered_dict['address'] = station_info['address']
    ordered_dict['city'] = station_info['city']
    ordered_dict['state'] = station_info['state']
    ordered_dict['zipcode'] = station_info['zipcode']
    ordered_dict['north_info'] = station_info['north_info']
    ordered_dict['south_info'] = station_info['south_info']
    ordered_dict['activities'] = station_info['activities']

    return ordered_dict


# TODO: Station info probably doesn't change so I only need to perform this computation once and shove it into PSQL
# TODO: Also find out how to hook flask up with PSQL on heroku
def get_station_info(station_abbr, bart_api_key):
    station_info_resp = requests.get(constants.STATION_INFO_ENDPOINT.format(station_abbr, bart_api_key))
    try:
        resp = xmltodict.parse(station_info_resp.content)
        return json.dumps({'message': resp['root']['message']['error']['details']}), constants.HTTP_BAD_REQUEST, \
               RESP_HEADER
    except Exception:
        station_info = json.loads(station_info_resp.content)['root']['stations']['station']

        del station_info['platform_info']

        station_info['lat'] = station_info['gtfs_latitude']
        station_info['lng'] = station_info['gtfs_longitude']
        del station_info['gtfs_latitude'], station_info['gtfs_longitude']

        station_info['description'] = station_info['intro']['#cdata-section']
        del station_info['intro']

        station_info['link'] = station_info['link']['#cdata-section']

        del station_info['cross_street']

        # TODO: this is repetitive. Make a method that handles creating the north_info/south_info dict
        if 'north_platforms' in station_info and 'north_routes' in station_info:
            north_info = {}
            north_info['platforms'] = station_info['north_platforms']['platform'] \
                if station_info['north_platforms'] != '' else []
            north_info['routes'] = station_info['north_routes']['route']
            station_info['north_info'] = north_info
            del station_info['north_platforms'], station_info['north_routes']

        south_info = {}
        south_info['platforms'] = station_info['south_platforms']['platform'] \
            if station_info['south_platforms'] != '' else []
        south_info['routes'] = station_info['south_routes']['route']
        station_info['south_info'] = south_info
        del station_info['south_platforms'], station_info['south_routes']

        # TODO: modularize this
        food_info = OrderedDict()
        food_info['activity_type'] = 'food'
        food_info['info'] = station_info['food']['#cdata-section']
        del station_info['food']

        shopping_info = OrderedDict()
        shopping_info['activity_type'] = 'shopping'
        shopping_info['info'] = station_info['shopping']['#cdata-section']
        del station_info['shopping']

        attraction_info = OrderedDict()
        attraction_info['activity_type'] = 'attraction'
        attraction_info['info'] = station_info['attraction']['#cdata-section']
        del station_info['attraction']

        activities = [food_info, shopping_info, attraction_info]
        station_info['activities'] = activities

        return json.dumps({'station_info': to_ordered_station_info_dict(station_info)}), constants.HTTP_STATUS_OK, \
               RESP_HEADER

