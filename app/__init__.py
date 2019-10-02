'''
    File name: __init__.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
    Description: App init
'''

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flasgger import Swagger
from dotenv import load_dotenv, find_dotenv

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)

    # Config
    load_dotenv(find_dotenv())
    app.config.from_object('config.' + os.getenv('FLASK_ENV'))

    # DB stuff
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    with app.app_context():
        # Routes
        from . import routes
        from . import errors
        from . import author
        from . import book

        # Development stuff
        if(app.config['FLASK_ENV'] == 'development'):
            # CLI
            from . import cli
            app.cli.add_command(cli.content_cli)
            app.cli.add_command(cli.s3upload)

            # Swagger
            swagger = Swagger()
            swagger.init_app(app)

        # Blueprints
        app.register_blueprint(routes.main_bp)

        # API Books enpoints
        app.add_url_rule(
            "/books", view_func=book.BooksApi.as_view("all_books_api")
            )
        app.add_url_rule(
            "/books/<book_id>", view_func=book.BookApi.as_view("books_api")
            )
        # API Authors enpoints
        app.add_url_rule(
            "/authors", view_func=author.AuthorsApi.as_view("all_authors_api")
            )
        app.add_url_rule(
            "/authors/<author_id>",
            view_func=author.AuthorApi.as_view("authors_api")
            )

        # Error handlers
        app.register_error_handler(404, errors.page_not_found)
        app.register_error_handler(400, errors.bad_request)
        app.register_error_handler(500, errors.internal_server_error)
        app.register_error_handler(401, errors.unauthorized)
        app.register_error_handler(405, errors.method_not_allowed)
        app.register_error_handler(409, errors.conflict)

        return app
