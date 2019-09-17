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
    CLOUDCUBE_ACCESS_KEY_ID = os.getenv('CLOUDCUBE_ACCESS_KEY_ID')
    CLOUDCUBE_SECRET_ACCESS_KEY = os.getenv('CLOUDCUBE_SECRET_ACCESS_KEY')
    CLOUDCUBE_URL = os.getenv('CLOUDCUBE_URL')
    CLOUDCUBE_REGION_NAME = os.getenv('CLOUDCUBE_REGION_NAME')
    CLOUDCUBE_BUCKET_NAME = os.getenv('CLOUDCUBE_BUCKET_NAME')
    CLOUDCUBE_FOLDER_PREFIX = os.getenv('CLOUDCUBE_FOLDER_PREFIX')


class development(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
    #    + os.path.join(basedir, 'app.sqlite3')
    CLOUDCUBE_ACCESS_KEY_ID = os.getenv('CLOUDCUBE_ACCESS_KEY_ID')
    CLOUDCUBE_SECRET_ACCESS_KEY = os.getenv('CLOUDCUBE_SECRET_ACCESS_KEY')
    CLOUDCUBE_URL = os.getenv('CLOUDCUBE_URL')
    CLOUDCUBE_REGION_NAME = os.getenv('CLOUDCUBE_REGION_NAME')
    CLOUDCUBE_BUCKET_NAME = os.getenv('CLOUDCUBE_BUCKET_NAME')
    CLOUDCUBE_FOLDER_PREFIX = os.getenv('CLOUDCUBE_FOLDER_PREFIX')
