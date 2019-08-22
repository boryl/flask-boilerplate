from dotenv import load_dotenv, find_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Load .env file
load_dotenv(find_dotenv())

class Config:
	"""Base config vars."""
	SECRET_KEY = os.getenv('SECRET_KEY')
	
    
class ProdConfig(Config):
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevConfig(Config):
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite3')
	SQLALCHEMY_TRACK_MODIFICATIONS = False