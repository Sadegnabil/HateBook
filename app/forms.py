# Import the datetime to be able to retrieve the time and Form with wtforms classes to be able to create the form and validate the data
from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired
import datetime

# Create the form class used to store the submitted login data
class Login(FlaskForm):
	# Username field
	username_login = TextField('username', validators = [DataRequired()])
	# Password field
	password_login = TextField('password', validators = [DataRequired()])
	# Location field
	location = TextField('location')


# Create the form class used to store the submitted register data before creating a new user
class Register(FlaskForm):
	# Username field
	username_register = TextField('username', validators = [DataRequired()])
	# Password field
	password_register = TextField('password', validators = [DataRequired()])
	# Surname field
	surname_register = TextField('surname', validators = [DataRequired()])
	# Name field
	name_register = TextField('name', validators = [DataRequired()])
	# Birth field
	birth_register = TextField('name', validators = [DataRequired()])


# Create the form class used to store the changements to the profile
class Profile(FlaskForm):
	# Name field
	name_profile = TextField('name', validators = [DataRequired()])
	# Surname field
	surname_profile = TextField('surname', validators = [DataRequired()])
	# Username field
	username_profile = TextField('username', validators = [DataRequired()])
	# Birth field
	birth_profile = TextField('birth', validators = [DataRequired()])
	# Password field
	password_profile = TextField('password', validators = [DataRequired()])
	# Confirm password field
	confirm_password_profile = TextField('confirm_password', validators = [DataRequired()])
	# Mood Sentence
	mood_profile = TextField('mood', validators = [DataRequired()])