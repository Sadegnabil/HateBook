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
	comments = db.relationship('Comments', backref='author', lazy='dynamic')
	reports = db.relationship('Reports', backref='author', lazy='dynamic')
	hates = db.relationship('Hates', backref='author', lazy='dynamic')



"""
Model representing a post with:
	- ID (Primary key)
	- Author
	- Date
	- Image link
	- Text
	- Hates
	- Comments
	- Reports
"""
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	date = db.Column(db.DateTime)
	image_link = db.Column(db.String(100))
	text = db.Column(db.String(500))
	hates = db.Column(db.Integer)
	comments = db.relationship('Comments', backref='post', lazy='dynamic')
	comments_number = db.Column(db.Integer, default=0)
	reports = db.relationship('Reports', backref='post', lazy='dynamic')
	reports_number = db.Column(db.Integer, default=0)
	hates_number = db.Column(db.Integer, default = 0)
	hates = db.relationship('Hates', backref='post', lazy='dynamic')



"""
Model representing a comment with:
	- ID (Primary key)
	- Author
	- Date
	- Text
	- Post ID
	- Reports
"""
class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime)
	text = db.Column(db.String(500))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	reports = db.relationship('Reports', backref='comment', lazy='dynamic')
	reports_number = db.Column(db.Integer, default=0)


class Reports(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))


class Hates(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))