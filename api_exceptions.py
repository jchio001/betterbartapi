import constants
import json


class MissingTokenException(Exception):
    http_code = constants.HTTP_BAD_REQUEST
    message = json.dumps({'message': constants.MISSING_API_KEY})

    def __init__(self):
        super(MissingTokenException, self).__init__()