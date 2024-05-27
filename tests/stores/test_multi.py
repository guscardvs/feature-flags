from unittest.mock import MagicMock, call

import pytest

from feature_flags.stores.multi import MultiStore


@pytest.fixture
def mock_store_1():
    return MagicMock()


@pytest.fixture
def mock_store_2():
    return MagicMock()


def test_multistore_save(mock_store_1, mock_store_2):
    # Initialize MultiStore with two mock stores
    multi_store = MultiStore(mock_store_1, mock_store_2)

    # Test saving flags
    multi_store.save('flag1', True)
    multi_store.save_bulk({'flag2': False})

    # Assert that save methods are called for both stores
    mock_store_1.save.assert_called_once_with('flag1', True)
    mock_store_1.save_bulk.assert_called_once_with({'flag2': False})
    mock_store_2.save.assert_called_once_with('flag1', True)
    mock_store_2.save_bulk.assert_called_once_with({'flag2': False})


def test_multistore_get(mock_store_1, mock_store_2):
    # Initialize MultiStore with two mock stores
    multi_store = MultiStore(mock_store_1, mock_store_2)

    # Test getting flags
    mock_store_1.get.return_value = False
    mock_store_2.get.return_value = True

    assert multi_store.get('flag1') is False

    mock_store_1.get.return_value = None
    assert multi_store.get('flag2') is True

    # Assert that get method is called for both stores and returns the correct value
    mock_store_1.get.assert_has_calls([call('flag1'), call('flag2')])
    mock_store_2.get.assert_called_once_with('flag2')


def test_multistore_get_all(mock_store_1, mock_store_2):
    # Initialize MultiStore with two mock stores
    multi_store = MultiStore(mock_store_1, mock_store_2)

    # Test getting all flags
    mock_store_1.get_all.return_value = {'flag1': False}
    mock_store_2.get_all.return_value = {'flag2': True}

    assert multi_store.get_all() == {'flag1': False, 'flag2': True}

    # Assert that get_all method is called for both stores and returns the correct value
    mock_store_1.get_all.assert_called_once()
    mock_store_2.get_all.assert_called_once()


def test_multistore_clear(mock_store_1, mock_store_2):
    # Initialize MultiStore with two mock stores
    multi_store = MultiStore(mock_store_1, mock_store_2)

    # Test clearing flags
    multi_store.clear()

    # Assert that clear method is called for both stores
    mock_store_1.clear.assert_called_once()
    mock_store_2.clear.assert_called_once()
