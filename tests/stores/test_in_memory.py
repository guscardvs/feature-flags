import pytest

from code_flags.stores.in_memory import InMemoryStore


@pytest.fixture
def in_memory_store():
    # Create an instance of InMemoryStore
    return InMemoryStore().singleton_ensure_new()


def test_save_and_get(in_memory_store):
    # Test saving and getting a single flag
    in_memory_store.save('flag1', True)
    assert in_memory_store.get('flag1') is True


def test_save_bulk_and_get_all(in_memory_store):
    # Test saving bulk flags and getting all flags
    flags = {'flag1': True, 'flag2': False}
    in_memory_store.save_bulk(flags)
    assert in_memory_store.get_all() == flags


def test_clear(in_memory_store):
    # Test clearing the store
    in_memory_store.save('flag1', True)
    in_memory_store.clear()
    assert in_memory_store.get_all() == {}
