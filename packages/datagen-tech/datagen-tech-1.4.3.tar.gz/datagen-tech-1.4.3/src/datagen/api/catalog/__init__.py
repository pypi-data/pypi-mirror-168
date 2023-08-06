import sys
from . import attributes
from .containers import CatalogsApiContainer
from .hooks.impl import OnLoad

_catalogs_api = CatalogsApiContainer().catalogs_api()

# Only works for Python 3.7 forward:
#
# def __getattr__(name):
#     return getattr(_catalogs_api, name)
#
#
# def __dir__():
#     catalog_api_public_props = [prop for prop in dir(_catalogs_api) if not prop.startswith("_")]
#     return [*catalog_api_public_props, "OnLoad"]
#
# Otherwise use:

setattr(_catalogs_api, "attributes", attributes)
sys.modules[__name__] = _catalogs_api
