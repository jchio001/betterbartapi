from decorators.decorators import CheckToken, CheckFields, LogReqHistory
from endpoint_logic import announcement_logic, estimate_logic, trip_logic, station_logic
from flask import Flask, redirect, request
from misc.api_exceptions import FailedBartRequestError, MissingFieldsError, MissingTokenError
from misc.constants import HTTP_FOUND, REDIRECT_URL

app = Flask(__name__)


# TODO: redirect this to the API documentation website when it exists
@app.route('/')
def index():
    return redirect(REDIRECT_URL, HTTP_FOUND)


@app.route('/announcements')
@CheckToken
def get_announcements():
    return announcement_logic.get_announcements()


@app.route('/stations')
@CheckToken
def get_stations():
    return station_logic.get_stations()


@app.route('/station/<station_abbr>')
@CheckToken
def get_station_info(station_abbr):
    return station_logic.get_station_info(station_abbr=station_abbr)


@app.route('/estimates/<orig_abbr>')
@CheckToken
def get_station_estimates(orig_abbr):
    return estimate_logic.get_estimates(orig_abbr=orig_abbr)


@app.route('/trip')
@CheckToken
@CheckFields({'orig', 'dest'})
def get_trips():
    return trip_logic.get_trips_resp(req_dict=request.args.to_dict())


@app.route('/trip/estimates')
@CheckToken
@CheckFields({'orig', 'dest'})
def get_route_estimates():
    return trip_logic.get_trip_with_estimates(req_dict=request.args.to_dict())


@app.errorhandler(MissingFieldsError)
def handle_missing_fields(missing_fields_exception):
    return missing_fields_exception.to_response()


@app.errorhandler(MissingTokenError)
def handle_no_token(missing_token_exception):
    return missing_token_exception.to_response()


@app.errorhandler(FailedBartRequestError)
@LogReqHistory
def handle_uncaught_failed_bart_req(failed_bart_req_error):
    return failed_bart_req_error.to_response()


if __name__ == "__main__":
    app.run()