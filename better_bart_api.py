from flask import Flask, request

import constants
import estimate_logic
import parameter_checks
import station_logic

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world!'


@app.route('/stations')
def get_stations():
    return station_logic.get_stations(bart_api_key=request.headers.get('X-API-KEY'))


@app.route('/station/<station_abbr>')
def get_station_info(station_abbr):
    return station_logic.get_station_info(station_abbr, bart_api_key=request.headers.get('X-API-KEY'))


# TODO: use a decorator instead to validate request args. And well to do all derpy validation logic...
@app.route('/estimates')
def get_station_estimates():
    req_dict = request.args.to_dict()
    invalid_key_set = parameter_checks.is_valid_estimate_req(req_dict)
    if not invalid_key_set:
        return estimate_logic.get_estimates(req_dict, bart_api_key=request.headers.get('X-API-KEY'))
    else:
        return constants.INVALID_REQUEST, constants.HTTP_BAD_REQUEST


if __name__ == "__main__":
    app.run()