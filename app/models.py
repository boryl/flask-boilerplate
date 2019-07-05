from app import db

class Author(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	
	def __repr__(self):
		return '<Author {}>'.format(self.name)
