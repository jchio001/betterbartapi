from clients.bart_api_client import bart_api_client
from collections import OrderedDict
from endpoint_logic import estimate_logic
from misc import constants
from misc.constants import RESP_HEADER
from misc.utils import string_to_epoch

import json


def format_leg(leg, fetch_estimates=False):
    pretty_leg_dict = OrderedDict()
    pretty_leg_dict['origin'] = leg['@origin']
    pretty_leg_dict['destination'] = leg['@destination']
    pretty_leg_dict['heading_towards'] = leg['@trainHeadStation']

    # converting arrival & departure times into epoch time
    pretty_leg_dict['departs'] = string_to_epoch(
        leg['@origTimeDate'].strip(),
        leg['@origTimeMin'])
    pretty_leg_dict['arrives'] = string_to_epoch(
        leg['@destTimeDate'].strip(),
        leg['@destTimeMin'])

    pretty_leg_dict['line'] = leg['@line']
    pretty_leg_dict['bikes_allowed'] = True if leg['@bikeflag'] == '1' else False

    if fetch_estimates:
        filtered_estimates_resp = estimate_logic.get_filtered_estimates(
            orig_abbr=pretty_leg_dict['origin'],
            final_dest_abbr=pretty_leg_dict['heading_towards'])

        if filtered_estimates_resp:
            pretty_leg_dict['limited'] = filtered_estimates_resp['limited']
            pretty_leg_dict['estimates'] = filtered_estimates_resp['estimates']
        else:
            pretty_leg_dict['limited'] = False
            pretty_leg_dict['estimates'] = []

    return pretty_leg_dict


# This method is to cleanly format a trip object and get real time estimates for each leg.
# Yes, there is a '@' in front of every key. No, I don't know why.
def format_trip(trip, fetch_estimates=False):
    pretty_trip_dict = OrderedDict()
    pretty_trip_dict['origin'] = trip['@origin']
    pretty_trip_dict['destination'] = trip['@destination']
    pretty_trip_dict['fare'] = trip['@fare']
    pretty_trip_dict['clipper'] = trip['@clipper']

    # converting arrival & departure times into epoch time
    pretty_trip_dict['departs'] = string_to_epoch(
        trip['@origTimeDate'].rstrip(),
        trip['@origTimeMin'])
    pretty_trip_dict['arrives'] = string_to_epoch(
        trip['@destTimeDate'].rstrip(),
        trip['@destTimeMin'])

    pretty_leg_list = []
    for leg in trip['leg']:
        pretty_leg_list.append(format_leg(leg=leg, fetch_estimates=fetch_estimates))

    pretty_trip_dict['trains'] = pretty_leg_list

    return pretty_trip_dict


def format_trips_resp(orig, dest, time_of_resp, formatted_trips):
    pretty_trip_with_estimates_resp = OrderedDict()
    pretty_trip_with_estimates_resp['origin'] = orig
    pretty_trip_with_estimates_resp['dest'] = dest
    pretty_trip_with_estimates_resp['resp_time'] = time_of_resp
    pretty_trip_with_estimates_resp['trips'] = formatted_trips

    return pretty_trip_with_estimates_resp


def format_trip_with_estimate_resp(orig, dest, time_of_resp, formatted_trip):
    pretty_trip_with_estimates_resp = OrderedDict()
    pretty_trip_with_estimates_resp['origin'] = orig
    pretty_trip_with_estimates_resp['dest'] = dest
    pretty_trip_with_estimates_resp['resp_time'] = time_of_resp
    pretty_trip_with_estimates_resp['trip'] = formatted_trip

    return pretty_trip_with_estimates_resp


def get_trips_resp(req_dict):
    trips_resp_dict = bart_api_client.get_trips(req_dict=req_dict)
    orig = trips_resp_dict['origin']
    dest = trips_resp_dict['destination']
    schedule = trips_resp_dict['schedule']
    time_of_resp = string_to_epoch(
        date_str=schedule['date'],
        time_str=schedule['time'])

    formatted_trips = []
    if schedule['request']['trip']:
        if isinstance(schedule['request']['trip'], list):
            formatted_trips = [map(lambda t : format_trip(trip=t, fetch_estimates=False), schedule['request']['trip'])]
        else:
            formatted_trips.append(
                format_trip(trip=schedule['request']['trip'],fetch_estimates=False))

    return json.dumps(
        format_trips_resp(
            orig=orig,
            dest=dest,
            time_of_resp=time_of_resp,
            formatted_trips=formatted_trips)
    ), constants.HTTP_STATUS_OK, RESP_HEADER


# designed to only return 1 trip instance!
def get_trip_with_estimates(req_dict):
    trips_resp_dict = bart_api_client.get_trips(req_dict=req_dict)
    orig = trips_resp_dict['origin']
    dest = trips_resp_dict['destination']
    schedule = trips_resp_dict['schedule']
    time_of_resp = string_to_epoch(
        date_str=schedule['date'],
        time_str=schedule['time'])

    trip = None
    if schedule['request']['trip']:
        if isinstance(schedule['request']['trip'], list):
            trip = schedule['request']['trip'][0]
        else:
            trip = schedule['request']['trip']

    formatted_trip = format_trip(trip=trip, fetch_estimates=True)

    return json.dumps(
        format_trip_with_estimate_resp(
            orig=orig,
            dest=dest,
            time_of_resp=time_of_resp,
            formatted_trip=formatted_trip)
    ), constants.HTTP_STATUS_OK, RESP_HEADER

