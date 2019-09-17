from flask import jsonify, abort, make_response, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from .models import db, Author, AuthorSchema
from .decorators import require_token


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
                jsonify(authors_schema.dump(authors).data), 200
                )

    @require_token
    def post(self):
        # Add new author
        payload = request.json
        new_author, errors = author_schema.load(payload)

        if(errors):
            abort(400, 'Can´t parse payload')

        try:
            db.session.add(new_author)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(
                409, 'Author {name} exists already'.
                format(name=new_author.name)
                )

        return make_response(jsonify(author_schema.dump(new_author).data), 201)


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
            return make_response(jsonify(author_schema.dump(author).data), 200)

    @require_token
    def put(self, author_id):
        # Update author
        payload = request.json

        update, errors = author_schema.load(payload)

        if(errors):
            abort(400, 'Can´t parse payload')

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
            jsonify(author_schema.dump(update_author).data),
            200
            )

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
