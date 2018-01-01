from collections import OrderedDict
from misc import constants
from misc.utils import string_to_epoch

import json
import logging
import requests
import xmltodict

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)


def format_announcements_resp(announcements_resp):
    pretty_announcement_resp = OrderedDict()
    # note: date & time for this endpoint is kinda dumb (example: 12/31/2017 17:49:00 PM PST)
    pretty_announcement_resp['time'] = string_to_epoch(
        date_str=announcements_resp['date'],
        time_str=announcements_resp['time'][:-7])
    pretty_announcement_resp['announcements'] = \
        {'announcements': list(map(lambda a: a['description']['#cdata-section'], announcements_resp['bsa']))}

    return pretty_announcement_resp


def get_announcements(bart_api_key):
    announcements_resp = requests.get(constants.ANNOUNCEMENTS_ENDPOINT.format(bart_api_key))
    if announcements_resp.status_code == constants.HTTP_STATUS_OK:
        try:
            announcements_resp = xmltodict.parse(announcements_resp.content)
            return {'error': announcements_resp['root']['message']['error']['details']}, constants.HTTP_BAD_REQUEST
        except Exception:
            announcements_resp = json.loads(announcements_resp.content)['root']
            return json.dumps(format_announcements_resp(announcements_resp)), constants.HTTP_STATUS_OK
    else:
        return {'error': constants.TRY_AGAIN_LATER}, 500