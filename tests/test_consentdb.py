"""
Examples on testing flaske with pytest and copied from https://gitlab.com/patkennedy79
"""
import pytest
from consentdb.models import db, ConsentRecord


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


@pytest.mark.parametrize("url, expected_status, expected_data",
                         [('/opt-outs/', 400, b'missing parameter'),
                          ('/opt-outs', 400, b'missing parameter'),
                          ('/opt-outs/?pid=1234', 200, b'Not found'),
                          ('/opt-outs/?pid=z1234', 200, b'Not found'),
                          ('/opt-outs/?pid=z12345', 200, b'Objection'),
                          ('/opt-outs?pid=z12345', 200, b'Objection')])
def test_opt_out(test_client, init_test_database, url, expected_status,
                 expected_data):
    """Test expected responses for old opt-out system

    This should return
    200 'not listed' if there is no objection
    200 'objection' if there is
    400 'Error' if you don't specify ?pid=
    """
    assert test_client.get(url).status_code == expected_status
    assert expected_data in test_client.get(url).data


@pytest.mark.parametrize("url, expected_status, expected_data",
                         [('/consent/', 400, b'Missing patient ID'),
                          ('/consent/1234', 400, b'record_not_found'),
                          ('/consent/z1234', 200, b'consent'),
                          ('/consent/z12345', 200, b'no_consent')])
def test_consent(test_client, init_test_database, url, expected_status,
                 expected_data):
    """Test expected responses for old opt-out system

    This should return
    200 'not listed' if there is no objection
    200 'objection' if there is
    400 'Error' if you don't specify ?pid=
    """
    assert test_client.get(url).status_code == expected_status
    assert test_client.get(url).data.startswith(expected_data)