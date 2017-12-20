from collections import OrderedDict

import constants
import json
import requests
import urllib
import xmltodict


def format_estimate_response(station_estimate_info):
    formatted_response = OrderedDict()
    formatted_response['name'] = station_estimate_info['name']
    formatted_response['abbr'] = station_estimate_info['abbr']
    formatted_response['destinations'] = station_estimate_info['etd']
    return formatted_response


def format_estimate_for_dest(estimate_for_dest):
    formatted_estimate_for_dest = OrderedDict()
    formatted_estimate_for_dest['destination'] = estimate_for_dest['destination']
    formatted_estimate_for_dest['abbr'] = estimate_for_dest['abbreviation']
    formatted_estimate_for_dest['limited'] = estimate_for_dest['limited']
    formatted_estimate_for_dest['estimate'] = estimate_for_dest['estimate']
    return formatted_estimate_for_dest


def format_estimate(estimate):
    formatted_estimate = OrderedDict()
    formatted_estimate['seconds'] = estimate['seconds']
    formatted_estimate['platform'] = estimate['platform']
    formatted_estimate['direction'] = estimate['direction']
    formatted_estimate['length'] = estimate['length']
    formatted_estimate['color'] = estimate['hexcolor']
    formatted_estimate['bikes_allowed'] = estimate['bikeflag']
    formatted_estimate['delay'] = estimate['delay']
    return formatted_estimate


def get_estimates(req_dict, bart_api_key):
    if bart_api_key is None:
        return json.dumps({'message': constants.MISSING_API_KEY}), constants.HTTP_BAD_REQUEST

    estimates_resp = requests.get(constants.ESTIMATES_BASE.format(bart_api_key) + urllib.urlencode(req_dict))
    if estimates_resp.status_code == constants.HTTP_STATUS_OK:
        try:
            resp = xmltodict.parse(estimates_resp.content)
            return json.dumps({'message': resp['root']['message']['error']['details']}), constants.HTTP_BAD_REQUEST
        except Exception:
            station_estimate_info = json.loads(estimates_resp.content)['root']['station'][0]
            estimates_for_all_dest = station_estimate_info['etd']

            formatted_estimates_for_dest = []
            for estimate_for_dest in estimates_for_all_dest:
                estimate_for_dest['limited'] = True if estimate_for_dest['limited'] == '1' else False

                formatted_estimates = []
                for estimate in estimate_for_dest['estimate']:
                    estimate['seconds'] = 0 if estimate['minutes'] == 'Leaving' else int(estimate['minutes']) * 60
                    estimate['platform'] = int(estimate['platform'])
                    estimate['length'] = int(estimate['length'])
                    estimate['bikeflag'] = True if estimate['bikeflag'] == '1' else False
                    estimate['delay'] = int(estimate['delay'])
                    formatted_estimates.append(format_estimate(estimate))

                estimate_for_dest['estimate'] = formatted_estimates
                formatted_estimates_for_dest.append(format_estimate_for_dest(estimate_for_dest))

            station_estimate_info['etd'] = formatted_estimates_for_dest
            return json.dumps(format_estimate_response(station_estimate_info)), constants.HTTP_STATUS_OK
    else:
        return json.dumps({'message': constants.TRY_AGAIN_LATER}), estimates_resp.status_code
