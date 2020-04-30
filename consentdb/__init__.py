"""Top-level package for Consent database."""
__author__ = """Sjoerd Kerkstra"""
__email__ = 'sjoerd.kerkstra@radboudumc.nl'
__version__ = '0.1.0'

from os import environ
from flask import Flask
from consentdb.consentdb import recipes_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI','sqlite:///:memory:')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from consentdb.models import db
    db.init_app(app)
    app.app_context().push()
    db.create_all()

    app.register_blueprint(recipes_blueprint)
    return app




