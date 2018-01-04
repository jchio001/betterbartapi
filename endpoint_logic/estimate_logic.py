from clients.bart_api_client import bart_api_client
from collections import OrderedDict
from misc import constants
from misc.api_exceptions import FailedBartRequestError
from misc.constants import RESP_HEADER

import json


def format_estimate_resp(station_estimate_info):
    formatted_response = OrderedDict()
    formatted_response['name'] = station_estimate_info['name']
    formatted_response['abbr'] = station_estimate_info['abbr']
    formatted_response['estimates'] = station_estimate_info['etd']
    return formatted_response


def format_estimate_for_dest(estimate_for_dest):
    formatted_estimate_for_dest = OrderedDict()
    formatted_estimate_for_dest['destination'] = estimate_for_dest['destination']
    formatted_estimate_for_dest['abbr'] = estimate_for_dest['abbreviation']
    formatted_estimate_for_dest['limited'] = estimate_for_dest['limited']
    formatted_estimate_for_dest['estimates'] = estimate_for_dest['estimate']
    return formatted_estimate_for_dest


def format_estimate(estimate):
    formatted_estimate = OrderedDict()
    formatted_estimate['seconds'] = 0 if estimate['minutes'] == 'Leaving' else int(estimate['minutes']) * 60
    formatted_estimate['platform'] = int(estimate['platform'])
    formatted_estimate['direction'] = estimate['direction']
    formatted_estimate['length'] = int(estimate['length'])
    formatted_estimate['color'] = estimate['hexcolor']
    formatted_estimate['bikes_allowed'] = True if estimate['bikeflag'] == '1' else False
    formatted_estimate['delay'] = int(estimate['delay'])
    return formatted_estimate


def get_estimates(orig_abbr):
    estimates = get_formatted_estimates(orig_abbr=orig_abbr)
    return json.dumps(estimates), constants.HTTP_STATUS_OK, RESP_HEADER


def get_formatted_estimates(orig_abbr):
    station_estimates_info = bart_api_client.get_estimates(orig_abbr=orig_abbr)[0]
    estimates_for_all_dest = station_estimates_info['etd']

    formatted_estimates_for_dest = []
    for estimate_for_dest in estimates_for_all_dest:
        estimate_for_dest['limited'] = True if estimate_for_dest['limited'] == '1' else False

        formatted_estimates = []
        for estimate in estimate_for_dest['estimate']:
            formatted_estimates.append(format_estimate(estimate))

        estimate_for_dest['estimate'] = formatted_estimates
        formatted_estimates_for_dest.append(format_estimate_for_dest(estimate_for_dest))

    station_estimates_info['etd'] = formatted_estimates_for_dest
    return format_estimate_resp(station_estimates_info)


def get_filtered_estimates(orig_abbr, final_dest_abbr):
    try:
        estimates = get_formatted_estimates(orig_abbr=orig_abbr)['estimates']

        for estimate in estimates:
            if estimate['abbr'] == final_dest_abbr:
                return estimate

        return {}
    except FailedBartRequestError:
        return {}
