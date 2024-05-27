import os

import pytest

from feature_flags.stores.sqlite import SQLiteStore


@pytest.fixture
def sqlite_store():
    # Create an instance of SQLiteStore with an in-memory database
    db_file = ':memory:'
    return SQLiteStore.singleton_ensure_new(db_file)


def test_save_and_get(sqlite_store):
    # Test saving and getting a single flag
    sqlite_store.save('flag1', True)
    assert sqlite_store.get('flag1') is True


def test_save_bulk_and_get_all(sqlite_store):
    # Test saving bulk flags and getting all flags
    flags = {'flag1': True, 'flag2': False}
    sqlite_store.save_bulk(flags)
    assert sqlite_store.get_all() == flags


def test_clear(sqlite_store):
    # Test clearing the store
    sqlite_store.save('flag1', True)
    sqlite_store.clear()
    assert sqlite_store.get_all() == {}


# Clean up the in-memory database after tests
def teardown_function():
    if os.path.exists(':memory:'):
        os.remove(':memory:')
