from api_exceptions import MissingTokenException
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
