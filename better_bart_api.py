from decorators import CheckToken
from flask import Flask, request

import constants
import estimate_logic
import json
import parameter_checks
import station_logic

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world!'


@app.route('/stations')
@CheckToken
def get_stations():
    return station_logic.get_stations(bart_api_key=request.headers.get('X-API-KEY'))


@app.route('/station/<station_abbr>')
@CheckToken
def get_station_info(station_abbr):
    return station_logic.get_station_info(station_abbr, bart_api_key=request.headers.get('X-API-KEY'))


@app.route('/estimates')
@CheckToken
def get_station_estimates():
    req_dict = request.args.to_dict()
    invalid_key_set = parameter_checks.is_valid_estimate_req(req_dict)
    if not invalid_key_set:
        return estimate_logic.get_estimates(req_dict, bart_api_key=request.headers.get('X-API-KEY'))
    else:
        return constants.INVALID_REQUEST, constants.HTTP_BAD_REQUEST


@app.errorhandler(401)
def handle_no_token(exception):
    return json.dumps({'message': constants.MISSING_API_KEY}), constants.HTTP_BAD_REQUEST

if __name__ == "__main__":
    app.run()