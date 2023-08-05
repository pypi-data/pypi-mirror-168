from .containers import CatalogsApiContainer
from .hooks.impl import OnLoad

_catalogs_api = CatalogsApiContainer().catalogs_api()


def __getattr__(name):
    return getattr(_catalogs_api, name)


def __dir__():
    catalog_api_public_props = [prop for prop in dir(_catalogs_api) if not prop.startswith("_")]
    return [*catalog_api_public_props, "OnLoad"]
