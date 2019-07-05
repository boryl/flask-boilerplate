from flask import Flask
from config import Config

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  from .views import author_bp
  app.register_blueprint(author_bp)

  return app
