"""
from . import db

class Author(db.Document):
    name = db.StringField()


class Book(db.Document):
    title = db.StringField()
    author = db.DocumentField(Author)
    year = db.IntField();
"""
class Author():
    name = ""


class Book():
    title = ""