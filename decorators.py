from api_exceptions import MissingFieldsException, MissingTokenException
from flask import request
from functools import wraps


def CheckToken(f):
    @wraps(f)
    # args = variable amount of values, kwargs = variable amount of key value pairs
    def check_token(*args, **kwargs):
        if request.headers.get('X-API-KEY') is None:
            raise MissingTokenException()
        else:
            return f(*args, **kwargs)
    return check_token


def ValidateFields(required_keys=set()):
    def validate_fields_wrapper(f):
        @wraps(f)
        def validate_fields(*args, **kwargs):
            request_dict = request.args.to_dict()
            missing_keys_set = set()
            for key in required_keys:
                if key not in request_dict:
                    missing_keys_set.add(key)

            if missing_keys_set:
                raise MissingFieldsException(missing_keys_set)
            else:
                return f(*args, **kwargs)
        return validate_fields
    return validate_fields_wrapper
