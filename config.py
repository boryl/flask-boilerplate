'''
    File name: config.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
    Description: Configuration
'''

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config vars."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECRET_TOKEN = os.getenv('SECRET_TOKEN')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_SWAGGER_UI_PATH = '/swagger'
    OPENAPI_URL_PREFIX = '/spec'
    OPENAPI_SWAGGER_UI_VERSION = '3.23.5'


class production(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class stage(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class development(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    STAGE_BUCKET_ACCESS_KEY_ID = os.getenv('STAGE_BUCKET_ACCESS_KEY_ID')
    STAGE_BUCKET_SECRET_ACCESS_KEY = os.getenv(
        'STAGE_BUCKET_SECRET_ACCESS_KEY'
        )
    BUCKET_REGION_NAME = os.getenv('BUCKET_REGION_NAME')
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    BUCKET_FOLDER_PREFIX = os.getenv('BUCKET_FOLDER_PREFIX')
    APP_CONTENT_FOLDER = os.path.join(basedir + '/resources/master/')
    APP_CONTENT_BUILD_FOLDER = os.path.join(
        basedir + '/resources/contentbuild/'
        )
    APP_CONTENT_FILE = 'appcontent.json'
    APP_CSV_FILE = 'source.csv'
