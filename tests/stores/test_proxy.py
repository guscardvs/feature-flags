import pytest

from feature_flags.stores.in_memory import InMemoryStore
from feature_flags.stores.proxy import ProxyStore


@pytest.fixture
def proxy_store():
    # Create an instance of ProxyStore with InMemoryStore as the proxied store
    return ProxyStore.singleton_ensure_new(
        InMemoryStore.singleton_ensure_new()
    )


def test_save_and_get(proxy_store):
    # Test saving and getting a single flag
    proxy_store.save('flag1', True)
    assert proxy_store.get('flag1') is True


def test_save_bulk_and_get_all(proxy_store):
    # Test saving bulk flags and getting all flags
    flags = {'flag1': True, 'flag2': False}
    proxy_store.save_bulk(flags)
    assert proxy_store.get_all() == flags


def test_clear(proxy_store):
    # Test clearing the store
    proxy_store.save('flag1', True)
    proxy_store.clear()
    assert proxy_store.get_all() == {}


def test_change(proxy_store):
    # Test changing the proxied store
    in_memory_store = InMemoryStore()
    proxy_store.change(in_memory_store)
    assert proxy_store._store is in_memory_store
