from datagen.api.datapoint.containers import DatapointApiClientContainer

_datapoint_api = DatapointApiClientContainer().datapoint_api()


def __getattr__(name):
    return getattr(_datapoint_api, name)


def __dir__():
    dp_api_public_props = [prop for prop in dir(_datapoint_api) if not prop.startswith("_")]
    return dp_api_public_props

