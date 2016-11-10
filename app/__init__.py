# Import the Flask virtual environment and SQLAlchemy for the database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Set the upload folder for the images
UPLOAD_FOLDER = 'app/static/images/profile_pictures'

# Create the flask app
app = Flask(__name__)
app.config.from_object('config')

# Generate a secret key
app.secret_key = os.urandom(24)

# Set the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the database
db = SQLAlchemy(app)

# Import views and models for the database
from app import views, models