"""Top-level package for Consent database."""
__author__ = """Sjoerd Kerkstra"""
__email__ = 'sjoerd.kerkstra@radboudumc.nl'
__version__ = '0.1.0'

from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI','sqlite:///:memory:')
db = SQLAlchemy(app)
