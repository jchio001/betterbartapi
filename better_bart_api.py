from api_exceptions import MissingFieldsError, MissingTokenException
from decorators import CheckToken, ValidateFields
from flask import Flask, request

import estimate_logic
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
@ValidateFields({'orig'})
def get_station_estimates():
    req_dict = request.args.to_dict()
    return estimate_logic.get_estimates(req_dict, bart_api_key=request.headers.get('X-API-KEY'))


@app.errorhandler(MissingFieldsError)
def missing_fields(missing_fields_exception):
    return missing_fields_exception.message, missing_fields_exception.http_code

@app.errorhandler(MissingTokenException)
def handle_no_token(missing_token_exception):
    return missing_token_exception.message, missing_token_exception.http_code


if __name__ == "__main__":
    app.run()