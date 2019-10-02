'''
    File name: utils.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-10-02
    Python Version: 3.7.4
    Description: Utility functions
'''

from marshmallow import ValidationError
from flask import request, abort


# Validate Json payload using provided Marshmallow schema
def validate_payload(validation_schema):
    payload = request.json
    try:
        result = validation_schema.load(payload)
    except ValidationError as err:
        error_message = ''
        i = 0
        for value in err.messages:
            if (i > 0):
                error_message += ' '
            error_message += 'Field \'' + value \
                + '\' - ' + (err.messages[value][0])
            i += 1
        abort(400, error_message)
    return (result)
