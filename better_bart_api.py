from decorators import CheckToken
from exceptions import MissingTokenException
from flask import Flask, request

import constants
import estimate_logic
import json
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
    return estimate_logic.get_estimates(req_dict, bart_api_key=request.headers.get('X-API-KEY'))


@app.errorhandler(MissingTokenException)
def handle_no_token():
    return json.dumps({'message': constants.MISSING_API_KEY}), constants.HTTP_BAD_REQUEST

if __name__ == "__main__":
    app.run()