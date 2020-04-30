"""
Examples on testing flaske with pytest and copied from https://gitlab.com/patkennedy79
"""
import pytest
from consentdb import create_app
from consentdb.models import db, ConsentRecord


@pytest.fixture(scope='module')
def test_client():
    """A flask test client with some debug settings."""
    flask_app = create_app()

    # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    flask_app.config['BCRYPT_LOG_ROUNDS'] = 4
     
    # Disable request error catching
    flask_app.config['TESTING'] = True
     
    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    flask_app.config['WTF_CSRF_ENABLED'] = False

    # expose built the Werkzeug test Client and handle context locals
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_test_database():
    """Init database and add some test data"""
    # Create the database and the database table
    db.create_all()

    # Create some records
    db.session.add(ConsentRecord(mdn='z1234', can_use=True))
    db.session.add(ConsentRecord(mdn='z12345', can_use=False))
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


def test_thing(test_client, init_test_database):
    response = test_client.post('/login')
    response = test_client.get('/opt-out-test')
    test_client.get('/opt-out/?pid=1234')
    test = 1
