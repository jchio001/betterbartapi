from flask import abort, request
from functools import wraps

import constants

def CheckToken(f):
    @wraps(f)
    # args = variable amount of values, kwargs = variable amount of key value pairs
    def check_token_method(*args, **kwargs):
        if request.headers.get('X-API-KEY') is None:
            abort(constants.HTTP_FORBIDDEN)
        else:
            return f(*args, **kwargs)
    return check_token_method