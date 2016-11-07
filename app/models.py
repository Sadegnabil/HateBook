# Import db to be able to create a database model
from app import db

class Users(db.Model):
	username = db.Column(db.String(20), primary_key = True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(20), default = "Enter your name")
	surname = db.Column(db.String(20), default = "Enter your name")
	birth = db.Column(db.String(20))
	registration_date = db.Column(db.String(20))
	country = db.Column(db.String(20))

