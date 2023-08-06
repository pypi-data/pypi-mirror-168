import sys

from . import assets
from .containers import DatapointApiClientContainer

_datapoint_api = DatapointApiClientContainer().datapoint_api()

# Only works for Python 3.7 forward:
#
# def __getattr__(name):
#     return getattr(_datapoint_api, name)
#
#
# def __dir__():
#     dp_api_public_props = [prop for prop in dir(_datapoint_api) if not prop.startswith("_")]
#     return dp_api_public_props
#
# Otherwise use:

setattr(_datapoint_api, "assets", assets)
sys.modules[__name__] = _datapoint_api
