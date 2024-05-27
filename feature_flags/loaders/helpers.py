from feature_flags.loaders.null import NullLoader
from feature_flags.loaders.proxy import ProxyLoader
from feature_flags.stores import Store
from feature_flags.utils import defer

from .loader import Loader

_default_loader = defer(ProxyLoader, NullLoader())


def get_loader() -> Loader:
    return ProxyLoader(_default_loader())


def initialize_store(loader: Loader, store: Store) -> None:
    flags = loader.load_all()
    store.save_bulk(flags)
