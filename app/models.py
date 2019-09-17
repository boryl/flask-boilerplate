from app import db, ma
from flask_marshmallow import Schema


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    # created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(
    #     db.DateTime,
    #     server_default=db.func.now(),
    #     server_onupdate=db.func.now()
    # )

    def __repr__(self):
        return '<Author {}>'.format(self.name)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey("author.id"), nullable=False
        )
    author = db.relationship("Author", backref="books")

    def __repr__(self):
        return '<Book {}>'.format(self.title)


class AuthorSchema(ma.ModelSchema):
    class Meta:
        model = Author
    books = ma.List(ma.HyperlinkRelated("books_api", "book_id"))


class BookPostSchema(ma.ModelSchema):
    class Meta:
        model = Book
        include_fk = True


class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book
    author = ma.HyperlinkRelated("authors_api", "author_id")


class TokenSchema(Schema):
    token = ma.Str(required=True)
