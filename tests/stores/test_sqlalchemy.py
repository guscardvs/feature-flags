import pytest

from feature_flags.stores.sqlalchemy import SQLAlchemyStore

# Create an in-memory SQLite database for testing
TEST_DB_URI = 'sqlite:///:memory:'


@pytest.fixture
def sqlalchemy_store():
    # Create an instance of SQLAlchemyStore with the test database
    return SQLAlchemyStore.singleton_ensure_new(TEST_DB_URI)


def test_save_and_get(sqlalchemy_store):
    # Test saving and getting a single flag
    sqlalchemy_store.save('flag1', True)
    assert sqlalchemy_store.get('flag1') is True


def test_save_bulk_and_get_all(sqlalchemy_store):
    # Test saving bulk flags and getting all flags
    flags = {'flag1': True, 'flag2': False}
    sqlalchemy_store.save_bulk(flags)
    assert sqlalchemy_store.get_all() == flags


def test_clear(sqlalchemy_store):
    # Test clearing the store
    sqlalchemy_store.save('flag1', True)
    sqlalchemy_store.clear()
    assert sqlalchemy_store.get_all() == {}
