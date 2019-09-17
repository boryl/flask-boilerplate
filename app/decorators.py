from functools import wraps
from flask import request, abort
from .models import TokenSchema
from flask import current_app as app


token_schema = TokenSchema()


def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Do something with your request here
        if(app.config['FLASK_ENV'] != 'sdevelopment'):
            payload = request.json
            token_json, errors = token_schema.load(payload)
            if(errors):
                abort(400, 'Missing access token')
            elif(token_json['token'] != app.config['SECRET_TOKEN']):
                abort(401, 'Can´t authorize token')
        return f(*args, **kwargs)
    return decorated_function
