'''
    File name: decorators.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
    Description: Decorators to require token and validate payload
'''

from functools import wraps
from flask import abort
from .models import TokenSchema
from flask import current_app as app
from .utils import validate_payload


def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if(app.config['FLASK_ENV'] != 'development'):
            result = validate_payload(TokenSchema())
            if(result['token'] != app.config['SECRET_TOKEN']):
                abort(401, 'Can´t authorize token')
        return f(*args, **kwargs)
    return decorated_function


def validate(schema):
    def validate_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = validate_payload(schema)
            args = args + (result,)
            return f(*args, **kwargs)
        return decorated_function
    return validate_decorator
