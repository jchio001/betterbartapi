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

# Resp Header
RESP_HEADER = {'Content-Type': 'application/json; charset=utf-8'}