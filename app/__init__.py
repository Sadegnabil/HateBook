# Import the Flask virtual environment and SQLAlchemy for the database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

UPLOAD_FOLDER = 'app/static/images/profile_pictures'


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

from app import views, models