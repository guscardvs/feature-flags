from unittest.mock import patch

import fakeredis
import pytest

from code_flags.stores.redis import RedisConfig, RedisStore


@pytest.fixture
def redis_store():
    # Create an instance of RedisStore with a mock Redis client
    with patch('redis.Redis', fakeredis.FakeRedis):
        return RedisStore.singleton_ensure_new(RedisConfig('localhost'))


def test_save_and_get(redis_store):
    # Test saving and getting a single flag
    redis_store.save('flag1', True)
    assert redis_store.get('flag1') is True


def test_save_bulk_and_get_all(redis_store):
    # Test saving bulk flags and getting all flags
    flags = {'flag1': True, 'flag2': False}
    redis_store.save_bulk(flags)
    assert redis_store.get_all() == flags


def test_clear(redis_store):
    # Test clearing the store
    redis_store.save('flag1', True)
    redis_store.clear()
    assert redis_store.get_all() == {}
