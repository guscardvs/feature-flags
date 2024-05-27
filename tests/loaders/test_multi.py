from unittest.mock import MagicMock

import pytest

from feature_flags.loaders.multi import MultiLoader


@pytest.fixture
def mock_loaders():
    # Create MagicMock instances to use as loaders
    loader1 = MagicMock()
    loader1.load.return_value = None
    loader1.load_all.return_value = {'flag1': 'value1', 'flag2': 'value2'}

    loader2 = MagicMock()
    loader2.load.return_value = 'Mocked Value'
    loader2.load_all.return_value = {
        'flag2': 'value2.5',
        'flag3': 'value3',
        'flag4': 'value4',
    }

    return loader1, loader2


def test_multi_loader_load(mock_loaders):
    # Create a MultiLoader instance with the mocked loaders
    multi_loader = MultiLoader(*mock_loaders)
    # Call the load method
    value = multi_loader.load('example_flag')
    # Ensure that the load method of each loader is called with the correct argument
    mock_loaders[0].load.assert_called_once_with('example_flag')
    mock_loaders[1].load.assert_called_once_with('example_flag')
    # Ensure that the returned value is the one returned by the second loader
    assert value == 'Mocked Value'


def test_multi_loader_load_all(mock_loaders):
    # Create a MultiLoader instance with the mocked loaders
    multi_loader = MultiLoader(*mock_loaders)
    # Call the load_all method
    flags = multi_loader.load_all()
    # Ensure that the load_all method of each loader is called
    mock_loaders[0].load_all.assert_called_once()
    mock_loaders[1].load_all.assert_called_once()
    # Ensure that the returned value is the combination of both loaders' results
    assert flags == {
        'flag1': 'value1',
        'flag2': 'value2',
        'flag3': 'value3',
        'flag4': 'value4',
    }


def test_multi_loader_refresh(mock_loaders):
    # Create a MultiLoader instance with the mocked loaders
    multi_loader = MultiLoader(*mock_loaders)
    # Call the refresh method
    multi_loader.refresh()
    # Ensure that the refresh method of each loader is called
    mock_loaders[0].refresh.assert_called_once()
    mock_loaders[1].refresh.assert_called_once()
