from datagen.api.datapoint.impl import DatapointApiClient
from dependency_injector import containers, providers


class DatapointApiClientContainer(containers.DeclarativeContainer):
    datapoint_api = providers.Singleton(DatapointApiClient)
