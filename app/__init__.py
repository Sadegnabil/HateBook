# Import the Flask virtual environment and SQLAlchemy for the database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Set the upload folder for the images
UPLOAD_FOLDER = 'app/static/images/profile_pictures'

# Create the flask app
app = Flask(__name__)
app.config.from_object('config')

# Set the admin page
from flask_admin import Admin
admin = Admin(app,template_mode='bootstrap3', base_template='admin.html')

# Generate a secret key
app.secret_key = os.urandom(24)

# Set the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the database
db = SQLAlchemy(app)

# Import views and models for the database
from app import views, models