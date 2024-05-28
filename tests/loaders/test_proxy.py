from pathlib import Path

import pytest

from code_flags.loaders.json import JsonLoader
from code_flags.loaders.proxy import ProxyLoader

RESOURCES_DIR = Path(__file__).parent.parent / 'resources'


@pytest.fixture
def proxy_loader():
    # Create a JsonLoader instance with the provided file path
    return ProxyLoader.singleton_ensure_new(
        JsonLoader(filename=RESOURCES_DIR / 'root_state.json')
    )


def test_load_flags(proxy_loader):
    # Test loading flags
    flags = proxy_loader.load_all()
    assert isinstance(flags, dict)
    assert len(flags) > 0  # Ensure flags are loaded


def test_load(proxy_loader):
    # Test loading a single flag
    value = proxy_loader.load('example_flag')
    assert isinstance(
        value, bool | int | float | str | type(None)
    )  # Ensure value is of a valid type


def test_load_all(proxy_loader):
    # Test loading all flags
    all_flags = proxy_loader.load_all()
    assert isinstance(all_flags, dict)
    assert len(all_flags) > 0  # Ensure flags are loaded


def test_refresh(proxy_loader):
    # Test refreshing flags
    initial_flags = proxy_loader.load_all()
    proxy_loader.refresh()
    assert (
        initial_flags == proxy_loader.load_all()
    )  # Flags should remain the same after refresh
