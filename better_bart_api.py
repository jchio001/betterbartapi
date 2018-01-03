from decorators.decorators import CheckToken, CheckFields
from endpoint_logic import announcement_logic, estimate_logic, route_logic, station_logic
from flask import Flask, request
from misc.api_exceptions import MissingFieldsError, MissingTokenException

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world!'


@app.route('/announcements')
@CheckToken
def get_announcements():
    return announcement_logic.get_announcements(bart_api_key=request.headers.get('X-API-KEY'))


@app.route('/stations')
@CheckToken
def get_stations():
    return station_logic.get_stations(bart_api_key=request.headers.get('X-API-KEY'))


@app.route('/station/<station_abbr>')
@CheckToken
def get_station_info(station_abbr):
    return station_logic.get_station_info(station_abbr=station_abbr, bart_api_key=request.headers.get('X-API-KEY'))


@app.route('/estimates/<orig_abbr>')
@CheckToken
def get_station_estimates(orig_abbr):
    return estimate_logic.get_estimates(orig_abbr=orig_abbr, bart_api_key=request.headers.get('X-API-KEY'))


@app.route('/trip')
@CheckToken
@CheckFields({'orig', 'dest'})
def get_trips():
    return route_logic.get_trips_resp(req_dict=request.args.to_dict(), bart_api_key=request.headers.get('X-API-KEY'))


@app.route('/trip/estimates')
@CheckToken
@CheckFields({'orig', 'dest'})
def get_route_estimates():
    return route_logic.get_trip_with_estimates(
        req_dict=request.args.to_dict(),
        bart_api_key=request.headers.get('X-API-KEY'))


@app.errorhandler(MissingFieldsError)
def missing_fields(missing_fields_exception):
    return missing_fields_exception.message, missing_fields_exception.http_code


@app.errorhandler(MissingTokenException)
def handle_no_token(missing_token_exception):
    return missing_token_exception.message, missing_token_exception.http_code


if __name__ == "__main__":
    app.run()