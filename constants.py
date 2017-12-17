# https status codes
HTTP_STATUS_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 401

# Error messages:
MISSING_API_KEY = 'Please pass in an API key through the header.'
TRY_AGAIN_LATER = 'Unable to process request. Please try again later'

# BART endpoints
STATIONS_ENDPOINT = 'http://api.bart.gov/api/stn.aspx?cmd=stns&json=y&key={}'
STATION_INFO_ENDPOINT = 'http://api.bart.gov/api/stn.aspx?cmd=stninfo&orig={}&key={}&json=y'