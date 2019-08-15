from app import db, ma

class Author(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False, unique=True)
	
	def __repr__(self):
		return '<Author {}>'.format(self.name)


class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
	author = db.relationship("Author", backref="books")
	
	def __repr__(self):
		return '<Book {}>'.format(self.title)

class AuthorSchema(ma.ModelSchema):
	
	class Meta:
		model = Author
	books = ma.List(ma.HyperlinkRelated("book_bp.list_book", "book_id"))
		
class BookPostSchema(ma.ModelSchema):
	
	class Meta:
		model = Book
		include_fk = True
	
class BookSchema(ma.ModelSchema):
	
	class Meta:
		model = Book
	
	author = ma.HyperlinkRelated("author_bp.list_author", "author_id")
	
	
			
		