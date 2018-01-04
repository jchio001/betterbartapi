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


class BartApiClient:
    def __init__(self):
        self.request_history = []
        self.bart_api_key = None

    def set_api_key(self, bart_api_key):
        self.bart_api_key = bart_api_key

    def log_req_history(self):
        logger.warn(json.dumps({'api_key': self.bart_api_key, 'req_history': self.request_history}))

    # generic code to make a request to BART API & to handle any errors that may occur
    # DO NOT use this method outside of bart_api_client.py!
    def get_resp_base(self, req_url):
        resp = requests.get(req_url)
        if resp.status_code == constants.HTTP_STATUS_OK:
            try:
                resp_dict = xmltodict.parse(resp.content)
                self.request_history.append({'url': req_url, 'status_code': constants.HTTP_BAD_REQUEST})
                raise FailedBartRequestError(http_status_code=constants.HTTP_BAD_REQUEST,
                                             message=resp_dict['root']['message']['error']['details'])
            except ExpatError:
                self.request_history.append({'url': req_url, 'status_code': constants.HTTP_STATUS_OK})
                return json.loads(resp.content)
        else:
            self.request_history.append({'url': req_url, 'status_code': resp.status_code})
            raise FailedBartRequestError(resp.status_code, constants.TRY_AGAIN_LATER)

    # fetches current BART announcements
    def get_announcements(self):
        announcement_req_url = ANNOUNCEMENTS_ENDPOINT.format(self.bart_api_key)
        return self.get_resp_base(announcement_req_url)['root']

    # fetches all stations available in BART
    def get_stations(self):
        stations_req_url = STATIONS_ENDPOINT.format(self.bart_api_key)
        return self.get_resp_base(stations_req_url)['root']['stations']['station']

    # fetches information about a station
    def get_station_info(self, station_abbr):
        station_info_req_url = STATION_INFO_ENDPOINT.format(station_abbr, self.bart_api_key)
        return self.get_resp_base(station_info_req_url)['root']['stations']['station']

    # fetches real time estimates for a station
    def get_estimates(self, orig_abbr):
        estimates_req_url = ESTIMATES_BASE.format(self.bart_api_key, orig_abbr)
        return self.get_resp_base(estimates_req_url)['root']['station']

    # fetches trips
    def get_trips(self, req_dict):
        route_cnt = 1
        if 'amount' in req_dict:
            route_cnt = req_dict['amount']
            del req_dict['amount']

        trips_req_url = TRIPS_ENDPOINT.format(self.bart_api_key, route_cnt) + urllib.urlencode(req_dict)
        return self.get_resp_base(trips_req_url)['root']


bart_api_client = BartApiClient()