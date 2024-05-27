from pathlib import Path

import pytest

from feature_flags.loaders.yaml import YamlLoader

RESOURCES_DIR = Path(__file__).parent.parent / 'resources'


@pytest.fixture
def yaml_loader():
    # Create a YamlLoader instance with the provided file path
    loader = YamlLoader(filename=RESOURCES_DIR / 'root_state.yaml')
    return loader


def test_load_flags(yaml_loader):
    # Test loading flags
    flags = yaml_loader.flags
    assert isinstance(flags, dict)
    assert len(flags) > 0  # Ensure flags are loaded


def test_load(yaml_loader):
    # Test loading a single flag
    value = yaml_loader.load('example_flag')
    assert isinstance(
        value, bool | int | float | str | type(None)
    )  # Ensure value is of a valid type


def test_load_all(yaml_loader):
    # Test loading all flags
    all_flags = yaml_loader.load_all()
    assert isinstance(all_flags, dict)
    assert len(all_flags) > 0  # Ensure flags are loaded


def test_refresh(yaml_loader):
    # Test refreshing flags
    initial_flags = yaml_loader.flags
    yaml_loader.refresh()
    assert (
        initial_flags == yaml_loader.flags
    )  # Flags should remain the same after refresh


def test_load_with_key():
    # Test loading flags with a specified key
    loader = YamlLoader(
        filename=RESOURCES_DIR / 'state.yaml', key='example_key'
    )
    flags = loader.flags
    assert isinstance(flags, dict)
    assert len(flags) > 0  # Ensure flags are loaded


def test_file_not_found():
    # Test behavior when the file is not found
    loader = YamlLoader(filename='non_existent_file.yaml')
    flags = loader.flags
    assert flags == {}  # Flags should be empty when file is not found
