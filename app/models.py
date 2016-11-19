# Import db to be able to create a database model
from app import db

"""
Model representing a user with:
	- ID (Primary key)
	- Name
	- Surname
	- Username
	- Password
	- Birth
	- Registration date

	From relationship:
	- Posts
	- Hates
	- Comments
	- Reports
"""
class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)

	name = db.Column(db.String(20))
	surname = db.Column(db.String(20))
	username = db.Column(db.String(20))
	password = db.Column(db.String(100))
	
	birth = db.Column(db.String(20))
	registration_date = db.Column(db.DateTime)

	posts = db.relationship('Posts', backref='author', lazy='dynamic')
	hates = db.relationship('Hates', backref='author', lazy='dynamic')
	comments = db.relationship('Comments', backref='author', lazy='dynamic')
	reports = db.relationship('Reports', backref='author', lazy='dynamic')
	


"""
Model representing a post with:
	- ID (Primary key)
	- Author ID
	- Date
	- Location
	- Text
	- Hates_number
	- Comments Number
	- Reports Number

	From relationship:
	- Author
	- Hates
	- Comments
	- Reports
"""
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	date = db.Column(db.DateTime)
	location = db.Column(db.String(50))
	text = db.Column(db.String(1000))

	hates = db.relationship('Hates', backref='post', lazy='dynamic')
	hates_number = db.Column(db.Integer, default = 0)

	comments = db.relationship('Comments', backref='post', lazy='dynamic')
	comments_number = db.Column(db.Integer, default=0)

	reports = db.relationship('Reports', backref='post', lazy='dynamic')
	reports_number = db.Column(db.Integer, default=0)



"""
Model representing a comment with:
	- ID (Primary key)
	- Author ID
	- Post ID
	- Date
	- Text
	- Reports Number

	From relationship:
	- Author
	- Post
	- Reports
"""
class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

	date = db.Column(db.DateTime)
	text = db.Column(db.String(500))
	
	reports = db.relationship('Reports', backref='comment', lazy='dynamic')
	reports_number = db.Column(db.Integer, default=0)



"""
Model representing a report with:
	- ID (Primary key)
	- Author ID
	- Post ID
	- COmment ID


	From relationship:
	- Author
	- Post
	- Comment
"""
class Reports(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))



"""
Model representing a hate with:
	- ID (Primary key)
	- Author ID
	- Post ID


	From relationship:
	- Author
	- Post
"""
class Hates(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))