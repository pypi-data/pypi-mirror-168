from datagen.components.dataset import DatasetConfig
from datagen.containers import DatagenContainer

_datagen = DatagenContainer().datagen()


def __getattr__(name):
    return getattr(_datagen, name)


def __dir__():
    datagen_props = [prop for prop in dir(_datagen) if not prop.startswith("_")]
    return [*datagen_props, "DatasetConfig"]
