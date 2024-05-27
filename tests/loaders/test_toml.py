from pathlib import Path

import pytest

from feature_flags.loaders.toml import TomlLoader

RESOURCES_DIR = Path(__file__).parent.parent / 'resources'


@pytest.fixture
def toml_loader():
    # Create a TomlLoader instance with the provided file path
    return TomlLoader(filename=RESOURCES_DIR / 'root_state.toml')


def test_load_flags(toml_loader):
    # Test loading flags
    flags = toml_loader.flags
    assert isinstance(flags, dict)
    assert len(flags) > 0  # Ensure flags are loaded


def test_load(toml_loader):
    # Test loading a single flag
    value = toml_loader.load('example_flag')
    assert isinstance(
        value, bool | int | float | str | type(None)
    )  # Ensure value is of a valid type


def test_load_all(toml_loader):
    # Test loading all flags
    all_flags = toml_loader.load_all()
    assert isinstance(all_flags, dict)
    assert len(all_flags) > 0  # Ensure flags are loaded


def test_refresh(toml_loader):
    # Test refreshing flags
    initial_flags = toml_loader.flags
    toml_loader.refresh()
    assert (
        initial_flags == toml_loader.flags
    )  # Flags should remain the same after refresh


def test_load_with_key():
    # Test loading flags with a specified key
    loader = TomlLoader(
        filename=RESOURCES_DIR / 'state.toml', table='example-key'
    )
    flags = loader.flags
    assert isinstance(flags, dict)
    assert len(flags) > 0  # Ensure flags are loaded


def test_file_not_found():
    # Test behavior when the file is not found
    loader = TomlLoader(filename='non_existent_file.toml')
    flags = loader.flags
    assert flags == {}  # Flags should be empty when file is not found
