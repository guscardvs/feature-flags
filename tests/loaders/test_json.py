from pathlib import Path

import pytest

from code_flags.loaders.json import JsonLoader

RESOURCES_DIR = Path(__file__).parent.parent / 'resources'


@pytest.fixture
def json_loader():
    # Create a JsonLoader instance with the provided file path
    return JsonLoader(filename=RESOURCES_DIR / 'root_state.json')


def test_load_flags(json_loader):
    # Test loading flags
    flags = json_loader.flags
    assert isinstance(flags, dict)
    assert len(flags) > 0  # Ensure flags are loaded


def test_load(json_loader):
    # Test loading a single flag
    value = json_loader.load('example_flag')
    assert isinstance(
        value, bool | int | float | str | type(None)
    )  # Ensure value is of a valid type


def test_load_all(json_loader):
    # Test loading all flags
    all_flags = json_loader.load_all()
    assert isinstance(all_flags, dict)
    assert len(all_flags) > 0  # Ensure flags are loaded


def test_refresh(json_loader):
    # Test refreshing flags
    initial_flags = json_loader.flags
    json_loader.refresh()
    assert (
        initial_flags == json_loader.flags
    )  # Flags should remain the same after refresh


def test_load_with_key():
    # Test loading flags with a specified key
    loader = JsonLoader(
        filename=RESOURCES_DIR / 'state.json', key='example_key'
    )
    flags = loader.flags
    assert isinstance(flags, dict)
    assert len(flags) > 0  # Ensure flags are loaded


def test_file_not_found():
    # Test behavior when the file is not found
    loader = JsonLoader(filename='non_existent_file.json')
    flags = loader.flags
    assert flags == {}  # Flags should be empty when file is not found
