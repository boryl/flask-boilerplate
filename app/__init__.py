import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flasgger import Swagger
from whitenoise import WhiteNoise

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
swagger = Swagger()

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
	
	swagger.init_app(app)
	
	
	
	with app.app_context():
		# Routes
		from . import routes
		from . import author
		from . import book
		
		# Blueprints
		app.register_blueprint(routes.main_bp)
		app.register_blueprint(author.author_bp, url_prefix='/authors')
		#app.register_blueprint(book.book_bp, url_prefix='/books')
		
		# API endpoints
		app.add_url_rule("/books", view_func=book.Books.as_view("all_books_api"))
		app.add_url_rule("/books/<entity>", view_func=book.Book.as_view("books_api"))
		
		app.wsgi_app = WhiteNoise(app.wsgi_app, root=os.path.join(os.path.dirname(__file__), 'static'), prefix='static/')
		
		return app


