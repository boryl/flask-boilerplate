'''
    File name: errors.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
    Description: Error routes
'''

from flask import jsonify, make_response


def page_not_found(e):
    return make_response(
        jsonify(error=str(e)), 404
        )


def bad_request(e):
    return make_response(
        jsonify(error=str(e)), 400
        )


def unauthorized(e):
    return make_response(
        jsonify(error=str(e)), 401
        )


def internal_server_error(e):
    return make_response(
        jsonify(error=str(e)), 500
    )


def method_not_allowed(e):
    return make_response(
        jsonify(error=str(e)), 405
    )


def conflict(e):
    return make_response(
        jsonify(error=str(e)), 409
    )
