"""
Examples on testing flaske with pytest and copied from https://gitlab.com/patkennedy79
"""
import pytest

from consentdb.admin import add_records
from consentdb.models import db, ConsentRecord


@pytest.fixture(scope='module')
def init_test_database():
    """Init database and add some test data"""
    # Create the database and the database table
    db.create_all()

    yield db  # this is where the testing happens!

    db.drop_all()


def test_add(test_client, init_test_database):

    add_records([ConsentRecord(mdn='z1234', can_use=True),
                 ConsentRecord(mdn='z12345', can_use=True),
                 ConsentRecord(mdn='z123456', can_use=True)])

    assert len(ConsentRecord.query.all()) == 3