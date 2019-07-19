from app import db, ma

class Author(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False, unique=True)
	
	def __repr__(self):
		return '<Author {}>'.format(self.name)


class AuthorSchema(ma.ModelSchema):
	
	class Meta:
		model = Author
	
		