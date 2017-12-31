# https status codes
HTTP_STATUS_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 401
HTTP_INTERNAL_SERVER_ERROR = 500

# Error messages:
MISSING_API_KEY = 'Please pass in an API key through the header.'
TRY_AGAIN_LATER = 'Unable to process request. Please try again later.'
INVALID_REQUEST = 'Invalid request.'
INVALID_PARAMS = 'Invalid request. Missing key(s): {}.'

# BART endpoints
ESTIMATES_BASE = 'http://api.bart.gov/api/etd.aspx?cmd=etd&key={}&orig={}&json=y'
STATIONS_ENDPOINT = 'http://api.bart.gov/api/stn.aspx?cmd=stns&json=y&key={}'
STATION_INFO_ENDPOINT = 'http://api.bart.gov/api/stn.aspx?cmd=stninfo&orig={}&key={}&json=y'
TRIPS_ENDPOINT = 'http://api.bart.gov/api/sched.aspx?cmd=depart&key={}&a={}&b=0&json=y&'
