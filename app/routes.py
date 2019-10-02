'''
    File name: routes.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
    Description: Main routes
'''

from flask import Blueprint


main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/')
def home():
    return ('Homepage')
