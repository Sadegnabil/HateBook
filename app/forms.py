# Import the datetime to be able to retrieve the time and Form with wtforms classes to be able to create the form and validate the data
from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired
import datetime

# Create the form class used to store the submitted data before putting them in the database
class Login(FlaskForm):
	# Title of the task
	username_login = TextField('username', validators = [DataRequired()])

	# Description of the task
	password_login = TextField('password', validators = [DataRequired()])


# Create the form class used to store the submitted data before putting them in the database
class Register(FlaskForm):
	# Title of the task
	username_register = TextField('username', validators = [DataRequired()])

	# Description of the task
	password_register = TextField('password', validators = [DataRequired()])