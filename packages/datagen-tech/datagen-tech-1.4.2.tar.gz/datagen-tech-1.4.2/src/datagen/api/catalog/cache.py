import abc
import datetime
import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional, Generic, TypeVar, List, Dict

from dependency_injector import providers

from datagen.api.catalog.attributes import AllOf, AnyOf, Exactly
from datagen.api.catalog.attributes import AssetAttributes

Asset = TypeVar("Asset")


@dataclass
class AssetCache(abc.ABC, Generic[Asset]):
    cache_file_name: str
    attributes_provider: providers.Callable
    last_refresh: datetime = field(default_factory=lambda: datetime.datetime.now() - datetime.timedelta(days=10))

    @property
    def outdated(self) -> bool:
        return self.last_refresh < datetime.datetime.now()

    def refresh(self, catalog_endpoint_response: List[dict]) -> None:
        ...

    @property
    def cache_file_path(self) -> Path:
        return Path(__file__).parent.joinpath("cache", self.cache_file_name)

    def query(self, asset_id: Optional[str], limit: Optional[int], **query_attributes) -> Dict[str, AssetAttributes]:
        asset_id_to_asset_attributes = self._get_asset_id_to_attributes()
        if asset_id is not None:
            try:
                return {asset_id: asset_id_to_asset_attributes[asset_id]}
            except KeyError:
                raise ValueError(f"Asset with id '{asset_id}' was not found in catalog")
        assets_by_attributes_match = self._get_matching_assets(asset_id_to_asset_attributes, query_attributes)
        if limit is not None:
            assets_keys = list(assets_by_attributes_match.keys())[:limit]
            return {k: assets_by_attributes_match[k] for k in assets_keys}
        else:
            return assets_by_attributes_match

    def _get_matching_assets(
        self, asset_id_to_asset_attributes: Dict[str, AssetAttributes], query_attributes: dict
    ) -> Dict[str, AssetAttributes]:
        return {
            asset_id: asset_attributes
            for asset_id, asset_attributes in asset_id_to_asset_attributes.items()
            if self._are_matching(asset_attributes, query_attributes)
        }

    @abc.abstractmethod
    def _get_asset_id_to_attributes(self) -> Dict[str, AssetAttributes]:
        ...

    def _are_matching(self, asset_attributes: AssetAttributes, query_attributes: dict) -> bool:
        matching = True
        for query_tag_name, query_attribute_value in query_attributes.items():
            asset_attribute_value, query_attribute_value = self._get_attributes_values(
                asset_attributes, query_tag_name, query_attribute_value
            )
            if isinstance(query_attribute_value, AllOf):
                matching &= all(v in asset_attribute_value for v in query_attribute_value)
            elif isinstance(query_attribute_value, AnyOf):
                matching &= any(v in asset_attribute_value for v in query_attribute_value)
            elif isinstance(query_attribute_value, Exactly):
                matching &= set(asset_attribute_value) == set(query_attribute_value)
        return matching

    @staticmethod
    def _get_attributes_values(
        asset_attributes: AssetAttributes, query_tag_name: str, query_tag_value: object
    ) -> tuple:
        asset_tag_value = getattr(asset_attributes, query_tag_name)
        if not isinstance(query_tag_value, (AllOf, AnyOf, Exactly)):
            query_tag_value = AllOf(query_tag_value)
        if not isinstance(asset_tag_value, list):
            asset_tag_value = [asset_tag_value]
        return asset_tag_value, query_tag_value


@dataclass
class InMemAssetCache(AssetCache):
    def __hash__(self):
        return hash(self.cache_file_name)

    @lru_cache(maxsize=None)
    def _get_asset_id_to_attributes(self) -> Dict[str, AssetAttributes]:
        with open(self.cache_file_path) as cache_file:
            asset_id_to_attributes_dict = json.load(cache_file)
        return {
            asset_id: self.attributes_provider(attributes_dict)
            for asset_id, attributes_dict in asset_id_to_attributes_dict.items()
        }
