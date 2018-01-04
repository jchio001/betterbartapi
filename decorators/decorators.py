from functools import wraps

from flask import request

from misc.api_exceptions import MissingFieldsError, MissingTokenError


# Used to verify if a user passed in their BART API token
def CheckToken(f):
    @wraps(f)
    # args = variable amount of values, kwargs = variable amount of key value pairs
    def check_token(*args, **kwargs):
        if request.headers.get('X-API-KEY') is None:
            raise MissingTokenError()
        else:
            return f(*args, **kwargs)
    return check_token


# Used to verify if the user has passed in value parameters in their request URL
def CheckFields(required_keys=set()):
    def validate_fields_wrapper(f):
        @wraps(f)
        def validate_fields(*args, **kwargs):
            request_dict = request.args.to_dict()
            # guaranteed each key in a dict is unique, so we don't need a set to enforce uniqueness!
            missing_keys_set = []
            for key in required_keys:
                if key not in request_dict:
                    missing_keys_set.append(key)

            if missing_keys_set:
                raise MissingFieldsError(missing_keys_set)
            else:
                return f(*args, **kwargs)
        return validate_fields
    return validate_fields_wrapper
