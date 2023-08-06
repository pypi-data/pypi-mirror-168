
from . import api
from .containers import DatagenContainer
from .components.dataset import DatasetConfig

_datagen = DatagenContainer().datagen()


# Only works for Python 3.7 forward:
#
# def __getattr__(name):
#     return getattr(_datagen, name)
#
#
# def __dir__():
#     datagen_props = [prop for prop in dir(_datagen) if not prop.startswith("_")]
#     return [*datagen_props, "DatasetConfig"]
#
# Otherwise use:

load = _datagen.load
explain = _datagen.explain

