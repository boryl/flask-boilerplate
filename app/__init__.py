import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.DevConfig')

#print(app.config['SECRET_KEY'])

# DB stuff
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Blueprints
from .views import author_bp
app.register_blueprint(author_bp, url_prefix="/author")


