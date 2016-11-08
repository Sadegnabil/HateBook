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


# Create the form class used to store the submitted register data before creating a new user
class Register(FlaskForm):
	# Username field
	username_register = TextField('username', validators = [DataRequired()])
	# Password field
	password_register = TextField('password', validators = [DataRequired()])


# Create the form class used to store the changements to the profile
class Profile(FlaskForm):
	name = TextField('name', validators = [DataRequired()])
	surname = TextField('surname', validators = [DataRequired()])
	username = TextField('username', validators = [DataRequired()])
	birth = TextField('birth', validators = [DataRequired()])
	registration_date = TextField('registration_date', validators = [DataRequired()])
	country = TextField('country', validators = [DataRequired()])