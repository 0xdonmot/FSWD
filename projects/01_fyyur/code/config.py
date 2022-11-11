import os
from flask_sqlalchemy import SQLAlchemy
from database_config import database_config
SECRET_KEY = os.urandom(32)
# Grab the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Setup database
db = SQLAlchemy()

# DATABASE URL
SQLALCHEMY_DATABASE_URI = database_config
