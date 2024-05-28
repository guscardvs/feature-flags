import pytest

from code_flags.stores.env import EnvironmentStore


@pytest.fixture
def environment_store(monkeypatch):
    # Mock the environment variables
    monkeypatch.setenv('FLAG_1', 'True')
    monkeypatch.setenv('FLAG_2', 'False')
    # Create an instance of EnvironmentStore with the mocked environment
    return EnvironmentStore.singleton_ensure_new()


def test_get(environment_store):
    # Test getting a single flag
    assert environment_store.get('FLAG_1') is True
    assert environment_store.get('FLAG_2') is False


def test_get_fallback(environment_store):
    # Test getting a flag that is not set in the environment
    assert environment_store.get('FLAG3') is None


def test_get_fallback_with_default_store(monkeypatch):
    # Mock the environment variables
    monkeypatch.delenv('FLAG_1', raising=False)
    monkeypatch.delenv('FLAG_2', raising=False)
    # Create an instance of EnvironmentStore with the mocked environment and a default store
    default_store = MockDefaultStore()
    environment_store = EnvironmentStore.singleton_ensure_new(
        fallback_store=default_store
    )
    # Test getting a flag that is not set in the environment
    assert environment_store.get('FLAG_1') is True
    assert environment_store.get('FLAG_2') is False
    # Ensure that the default store's get method was called
    assert default_store.callcounter == 2  # noqa: PLR2004


def test_get_with_key_transform(environment_store):
    # Test getting a flag with key transformation
    assert environment_store.get('flag-1') is True
    assert environment_store.get('flag_2') is False


def test_get_with_missing_transform(environment_store):
    # Test getting a flag with a transform that doesn't match any environment variable
    assert environment_store.get('flag3') is None


# Define a mock default store for testing fallback behavior
class MockDefaultStore:
    def __init__(self) -> None:
        self.callcounter = 0

    def get(self, flag):
        self.callcounter += 1
        return True if flag == 'FLAG_1' else False
