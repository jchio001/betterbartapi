import constants
import json


class MissingFieldsError(Exception):
    http_code = constants.HTTP_BAD_REQUEST

    def __init__(self, missing_keys):
        self.message = json.dumps({'message': self.format_missing_fields_message(missing_keys)})
        super(MissingFieldsError, self).__init__()

    @staticmethod
    def format_missing_fields_message(missing_keys):
        if not missing_keys:
            raise ValueError

        return constants.INVALID_PARAMS.format(', '.join(missing_keys))


class MissingTokenException(Exception):
    http_code = constants.HTTP_BAD_REQUEST
    message = json.dumps({'message': constants.MISSING_API_KEY})

    def __init__(self):
        super(MissingTokenException, self).__init__()
