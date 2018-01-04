from clients import bart_api_client
from collections import OrderedDict
from misc import constants
from misc.constants import RESP_HEADER
from misc.utils import string_to_epoch

import json


def format_announcements_resp(announcements_resp):
    pretty_announcement_resp = OrderedDict()
    # note: date & time for this endpoint is kinda dumb (example: 12/31/2017 17:49:00 PM PST)
    pretty_announcement_resp['time'] = string_to_epoch(
        date_str=announcements_resp['date'],
        time_str=announcements_resp['time'][:-7])
    pretty_announcement_resp['announcements'] = \
        {'announcements': [map(lambda a: a['description']['#cdata-section'], announcements_resp['bsa'])]}

    return pretty_announcement_resp


def get_announcements(bart_api_key):
    formatted_announcements_resp = format_announcements_resp(bart_api_client.get_announcements(bart_api_key))
    return json.dumps(formatted_announcements_resp), constants.HTTP_STATUS_OK, RESP_HEADER