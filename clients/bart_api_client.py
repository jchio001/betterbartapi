from misc import constants
from misc.api_exceptions import FailedBartRequestError
from xml.parsers.expat import ExpatError

import json
import logging
import requests
import urllib
import xmltodict

ANNOUNCEMENTS_ENDPOINT = 'https://api.bart.gov/api/bsa.aspx?cmd=bsa&key={}&json=y'
ESTIMATES_BASE = 'https://api.bart.gov/api/etd.aspx?cmd=etd&key={}&orig={}&json=y'
STATIONS_ENDPOINT = 'https://api.bart.gov/api/stn.aspx?cmd=stns&json=y&key={}'
STATION_INFO_ENDPOINT = 'https://api.bart.gov/api/stn.aspx?cmd=stninfo&orig={}&key={}&json=y'
TRIPS_ENDPOINT = 'https://api.bart.gov/api/sched.aspx?cmd=depart&key={}&a={}&b=0&json=y&'

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)

# This file represents a client that interacts with BART API.


# generic code to make a request to BART API & to handle any errors that may occur
# DO NOT use this method outside of bart_api_client.py!
def get_resp_base(req_url):
    resp = requests.get(req_url)
    if resp.status_code == constants.HTTP_STATUS_OK:
        try:
            resp_dict = xmltodict.parse(resp.content)
            raise FailedBartRequestError(http_status_code=constants.HTTP_BAD_REQUEST,
                                         message=resp_dict['root']['message']['error']['details'])
        except ExpatError:
            return json.loads(resp.content)
    else:
        raise FailedBartRequestError(resp.status_code, constants.TRY_AGAIN_LATER)

# fetches current BART announcements
def get_announcements(bart_api_key):
    announcement_req_url = ANNOUNCEMENTS_ENDPOINT.format(bart_api_key)
    return get_resp_base(announcement_req_url)['root']


# fetches all stations available in BART
def get_stations(bart_api_key):
    stations_req_url = STATIONS_ENDPOINT.format(bart_api_key)
    return get_resp_base(stations_req_url)['root']['stations']['station']


# fetches information about a station
def get_station_info(station_abbr, bart_api_key):
    station_info_req_url = STATION_INFO_ENDPOINT.format(station_abbr, bart_api_key)
    return get_resp_base(station_info_req_url)['root']['stations']['station']


# fetches real time estimates for a station
def get_estimates(orig_abbr, bart_api_key):
    estimates_req_url = ESTIMATES_BASE.format(bart_api_key, orig_abbr)
    return get_resp_base(estimates_req_url)['root']['station']


# fetches trips
def get_trips(req_dict, bart_api_key):
    route_cnt = 1
    if 'amount' in req_dict:
        route_cnt = req_dict['amount']
        del req_dict['amount']

    trips_req_url = TRIPS_ENDPOINT.format(bart_api_key, route_cnt) + urllib.urlencode(req_dict)
    return get_resp_base(trips_req_url)['root']