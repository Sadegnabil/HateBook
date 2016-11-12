# Import db to be able to create a database model
from app import db

"""
Model representing a user with:
	- Username (Primary key)
	- Name
	- Surname
	- Password
	- Birth
	- Registration date
	- Country
"""
class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20))
	password = db.Column(db.String(100))
	name = db.Column(db.String(20))
	surname = db.Column(db.String(20))
	birth = db.Column(db.String(20))
	registration_date = db.Column(db.DateTime)
	country = db.Column(db.String(50))
	posts = db.relationship('Posts', backref='author', lazy='dynamic')



"""
Model representing a post with:
	- ID (Primary key)
	- Author
	- Date
	- Image link
	- Text
	- Hates
	- Comments
	- Flags
"""
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	date = db.Column(db.DateTime)
	image_link = db.Column(db.String(100))
	text = db.Column(db.String(500))
	hates = db.Column(db.Integer)
	comments = db.Column(db.Integer)
	flags = db.Column(db.Integer)



"""
Model representing a comment with:
	- ID (Primary key)
	- Author
	- Date
	- Text
	- Post ID
	- Flags
"""
class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(20))
	date = db.Column(db.DateTime)
	text = db.Column(db.String(500))
	postID = db.Column(db.Integer)
	flags = db.Column(db.Integer)