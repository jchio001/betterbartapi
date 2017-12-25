import constants
import json


class MissingFieldsException(Exception):
    http_code = constants.HTTP_BAD_REQUEST

    def __init__(self, missing_keys_set=set()):
        self.message = json.dumps({'message': constants.INVALID_PARAMS.format(missing_keys_set)})
        super(MissingFieldsException, self).__init__()


class MissingTokenException(Exception):
    http_code = constants.HTTP_BAD_REQUEST
    message = json.dumps({'message': constants.MISSING_API_KEY})

    def __init__(self):
        super(MissingTokenException, self).__init__()
