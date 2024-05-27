from unittest.mock import MagicMock

import pytest

from feature_flags.loaders.store import StoreLoader


@pytest.fixture
def mock_store():
    # Create a MagicMock instance to use as a store
    return MagicMock()


def test_load(mock_store):
    # Create an instance of StoreLoader with the mocked store
    loader = StoreLoader(mock_store)
    # Test loading a single flag
    loader.load('flag1')
    # Ensure that the store's get method was called with the correct argument
    mock_store.get.assert_called_once_with('flag1')


def test_load_all(mock_store):
    # Create an instance of StoreLoader with the mocked store
    loader = StoreLoader(mock_store)
    # Test loading all flags
    loader.load_all()
    # Ensure that the store's get_all method was called
    mock_store.get_all.assert_called_once()


def test_refresh(mock_store):
    # Create an instance of StoreLoader with the mocked store
    loader = StoreLoader(mock_store)
    # Test refreshing the loader
    loader.refresh()
    # Ensure that no interaction with the store occurred during refresh
    assert not mock_store.called
