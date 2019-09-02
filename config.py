from dotenv import load_dotenv, find_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Load .env file
load_dotenv(find_dotenv())

class Config:
	"""Base config vars."""
	SECRET_KEY 											= os.getenv('SECRET_KEY')
	SQLALCHEMY_TRACK_MODIFICATIONS 	= False
	OPENAPI_VERSION 								= '3.0.2'
	OPENAPI_SWAGGER_UI_PATH 				= '/swagger'
	OPENAPI_URL_PREFIX 							= '/spec'
	OPENAPI_SWAGGER_UI_VERSION 			= '3.23.5'
	ENV 														= os.getenv('ENV')
	
    
class ProdConfig(Config):
	DEBUG 													= False
	TESTING 												= False
	SQLALCHEMY_DATABASE_URI 				= os.getenv('DATABASE_URL')
	

class DevConfig(Config):
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI 				= 'sqlite:///' + os.path.join(basedir, 'app.sqlite3')
	CLOUDCUBE_ACCESS_KEY_ID 				= os.getenv('CLOUDCUBE_ACCESS_KEY_ID')
	CLOUDCUBE_SECRET_ACCESS_KEY 		= os.getenv('CLOUDCUBE_SECRET_ACCESS_KEY')
	CLOUDCUBE_URL 									= os.getenv('CLOUDCUBE_URL')
	CLOUDCUBE_REGION_NAME 					= os.getenv('CLOUDCUBE_REGION_NAME')
	CLOUDCUBE_BUCKET_NAME 					= os.getenv('CLOUDCUBE_BUCKET_NAME')
	CLOUDCUBE_FOLDER_PREFIX 				= os.getenv('CLOUDCUBE_FOLDER_PREFIX')