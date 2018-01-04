import constants
import json


class MissingFieldsError(Exception):
    def __init__(self, missing_keys):
        super(MissingFieldsError, self).__init__()
        self.message = self.format_missing_fields_message(missing_keys)

    @staticmethod
    def format_missing_fields_message(missing_keys):
        if not missing_keys:
            raise ValueError

        return constants.INVALID_PARAMS.format(', '.join(missing_keys))

    def to_response(self):
        return json.dumps({'message': self.message}), constants.HTTP_BAD_REQUEST, constants.RESP_HEADER


class MissingTokenError(Exception):
    def __init__(self):
        super(MissingTokenError, self).__init__()

    def to_response(self):
        return json.dumps({'message': constants.MISSING_API_KEY}), constants.HTTP_BAD_REQUEST, constants.RESP_HEADER


class FailedBartRequestError(Exception):
    def __init__(self, http_status_code, message):
        super(FailedBartRequestError, self).__init__()
        self.http_status_code = http_status_code
        self.message = message

    def to_response(self):
        return json.dumps({'message': self.message}), self.http_status_code, constants.RESP_HEADER


