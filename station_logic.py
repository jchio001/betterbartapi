import constants
import json
import requests
import xmltodict

def get_stations(bart_api_key):
    if bart_api_key is None:
        return json.dumps({'message': constants.MISSING_API_KEY}), constants.HTTP_BAD_REQUEST

    stations_resp = requests.get(constants.STATIONS_ENDPOINT.format(bart_api_key))
    # NOTE: Bart API apparently returns 200 for literally every case ever. So, we need to check what's the appropriate
    # course of action by checking to see if it's a XML response or a JSON response
    if stations_resp.status_code == constants.HTTP_STATUS_OK:
        try:
            resp = xmltodict.parse(stations_resp.content)
            return json.dumps({'message': resp['root']['message']['error']['details']}), constants.HTTP_BAD_REQUEST
        except Exception:
            return json.dumps({'stations': json.loads(stations_resp.content)['root']['stations']['station']})
    else:
        return json.dumps({'message': constants.TRY_AGAIN_LATER}), stations_resp.status_code