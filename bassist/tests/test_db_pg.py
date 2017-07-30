import pytest

import bassist.flavor.db_pg as db

db = db.DB()


def test_record_flavor_returns_id():
    flavor_name = 'ubuntu-14.04'
    id = db.record_flavor(flavor_name)
    assert id == 'hi'
