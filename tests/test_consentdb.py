import pytest
from consentdb import db, app
from consentdb.consentdb import ConsentRecord

from consentdb import consentdb

# Excellent examples on flask testing with pytest from https://gitlab.com/patkennedy79


@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    """
    # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    BCRYPT_LOG_ROUNDS = 4
     
    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True
     
    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False
    """


    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    db.session.add(ConsentRecord(mdn='z1234', can_use=True))
    db.session.add(ConsentRecord(mdn='z12345', can_use=False))
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


def test_thing(test_client, init_database):
    response = test_client.post('/login')
    response = test_client.get('/opt-out-test')
    test = 1
