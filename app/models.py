'''
    File name: models.py
    Projekt: Flask boilerplate
    Author: Björn-Olle Rylander
    Date created: 2019-07-07
    Python Version: 3.7.4
    Description: Database models and schemas
'''

from app import db, ma
from flask_marshmallow import Schema
from marshmallow import INCLUDE, EXCLUDE, validates, validate, ValidationError
import os


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
        unknown = EXCLUDE
    books = ma.List(ma.HyperlinkRelated("books_api", "book_id"))


class BookPostSchema(ma.ModelSchema):
    class Meta:
        model = Book
        unknown = EXCLUDE
        include_fk = True


class BookSchema(ma.ModelSchema):
    class Meta:
        model = Book
        unknown = EXCLUDE
    author = ma.HyperlinkRelated("authors_api", "author_id")


class TokenSchema(Schema):
    class Meta:
        unknown = INCLUDE
    token = ma.Str(required=True)


class ContentSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    id = ma.Int(
        required=True,
        error_messages={"invalid": "Missing ID number"},
        )
    content = ma.Str(
        required=True,
        validate=validate.Length(min=1, error='Missing Content'),
        )
    group = ma.Int(
        required=True,
        error_messages={"invalid": "Missing group number"},
        )
    question = ma.Str(
        required=True,
        validate=validate.Length(min=1, error='Missing Content'),
        )
    image = ma.Str(required=True)

    @validates("image")
    def validate_quantity(self, value):
        if (not os.path.isfile('resources/master/images/' + value)):
            raise ValidationError("Missing file: " + value)
