from feature_flags.loaders import Loader, ProxyLoader
from feature_flags.loaders.helpers import initialize_store
from feature_flags.loaders.store import StoreLoader
from feature_flags.stores import ProxyStore, Store, get_store


def initialize(loader: Loader | None = None, store: Store | None = None):
    store = ProxyStore(store or get_store())
    if loader is None:
        loader = StoreLoader(store)
    loader = ProxyLoader(loader)
    initialize_store(loader, store)
