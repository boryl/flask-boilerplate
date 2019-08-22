import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
	app = Flask(__name__)
	if(os.getenv('ENV') == 'PROD'):
		config = 'ProdConfig'
	else:
		config = 'DevConfig'
	app.config.from_object('config.' + config)
	
	# DB stuff
	db.init_app(app)
	migrate.init_app(app, db)
	ma.init_app(app)
	
	with app.app_context():
		# Blueprints
		from . import routes
		from . import author
		from . import book
		
		app.register_blueprint(routes.main_bp)
		app.register_blueprint(author.author_bp, url_prefix='/author')
		app.register_blueprint(book.book_bp, url_prefix='/book')
		
		return app


