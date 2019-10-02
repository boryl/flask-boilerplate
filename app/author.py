'''
    File name: author.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
    Description: API template
'''

from flask import jsonify, abort, make_response
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from .models import db, Author, AuthorSchema
from .decorators import require_token, validate


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


# Operations on all authors
class AuthorsApi(MethodView):
    @require_token
    def get(self):
        # Get all authors
        authors = Author.query.order_by(Author.name).all()
        if authors is None:
            abort(404, 'Books not found')
        else:
            return make_response(
                jsonify(authors_schema.dump(authors)), 200
                )

    @require_token
    @validate(author_schema)
    def post(self, new_author):
        # Add new author
        try:
            db.session.add(new_author)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(
                409, 'Author {name} exists already'.
                format(name=new_author.name)
                )

        return make_response(jsonify(author_schema.dump(new_author)), 201)


# Operations on a single author
class AuthorApi(MethodView):
    @require_token
    def get(self, author_id):
        # Get one author
        author = Author.query.get(author_id)

        if author is None:
            abort(
                404, 'Author not found for id {id}'
                .format(id=author_id), 404
                )
        else:
            return make_response(jsonify(author_schema.dump(author)), 200)

    @require_token
    @validate(author_schema)
    def put(self, update, author_id):
        # Update author
        update_author = Author.query.get(author_id)

        if update_author is None:
            abort(
                404, 'Author not found for id {id}'.
                format(id=author_id)
            )
        else:
            update.id = update_author.id
            try:
                db.session.merge(update)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                abort(
                    409, 'Author {name} exists already'.
                    format(name=update_author.name)
                    )

        return make_response(
            jsonify(author_schema.dump(update_author)),
            200
            )

    @require_token
    def delete(self, author_id):
        # Delete author
        author = Author.query.get(author_id)

        if author is None:
            abort(
                404, 'Author not found for id: {id}'.
                format(id=author_id)
            )
        else:
            db.session.delete(author)
            db.session.commit()
            return make_response(
                    jsonify(message='Author {id} deleted'.
                            format(id=author_id)),
                    200
                    )
