from rich import pretty as pretty_rich

from dataclasses import dataclass, field
from typing import Optional, TypeVar, Generic, Union, Dict, List

from dependency_injector import providers
from pydantic import Extra

from datagen.api.catalog.hooks.impl import AssetLoadingHooks, OnLoad
from datagen.api.catalog.cache import AssetCache
from datagen.api.catalog.attributes import AssetAttributes
from datagen.api.datapoint.assets import Hair, Human, Eyes, Glasses, Mask, Background

Asset = TypeVar("Asset")


@dataclass
class CatalogEndpoint:
    url: str

    def fetch(self) -> List[dict]:
        ...


@dataclass
class AssetCatalog(Generic[Asset]):
    asset_provider: providers.Provider
    asset_cache: AssetCache[Asset]
    hooks: AssetLoadingHooks[Asset] = field(default_factory=AssetLoadingHooks)
    catalog_endpoint: Optional[CatalogEndpoint] = field(default=None)

    def get(
        self, id: Optional[str] = None, limit: Optional[int] = None, load_assets: bool = True, **attributes
    ) -> Union[Asset, List[Asset], Dict[str, AssetAttributes]]:
        if id is not None:
            return self._get_asset_by_id(id)
        else:
            return self._get_assets(limit, load_assets, **attributes)

    def _get_assets(
        self, limit: Optional[int], load_assets: bool, **attributes
    ) -> Union[Asset, List[Asset], Dict[str, AssetAttributes]]:
        assets = self._query(limit=limit, **attributes)
        assets = self._load(assets) if load_assets else assets
        return assets[0] if limit == 1 else assets

    def _get_asset_by_id(self, id: str) -> Asset:
        [(asset_id, asset_attributes)] = self._query(id).items()
        return self._load_asset(asset_id, asset_attributes)

    def _load(self, assets: Dict[str, AssetAttributes]) -> List[Asset]:
        loaded_assets = []
        for asset_id, asset_attributes in assets.items():
            asset = self._load_asset(asset_id, asset_attributes)
            loaded_assets.append(asset)
        return loaded_assets

    def _load_asset(self, asset_id: str, attributes: AssetAttributes) -> Asset:
        asset = self.asset_provider(id=asset_id)
        self._add_attributes(asset, attributes)
        self.hooks.apply_all(asset)
        return asset

    def _add_attributes(self, asset, attributes):
        asset.Config.extra = Extra.allow
        asset.attributes = attributes
        asset.Config.extra = Extra.forbid

    def count(self, **attributes) -> int:
        return len(self._query(**attributes))

    def _query(self, id: Optional[str] = None, limit: Optional[int] = None, **attributes) -> Dict[str, AssetAttributes]:
        if self.asset_cache.outdated and self.catalog_endpoint is not None:
            self.asset_cache.refresh(self.catalog_endpoint.fetch())
        return self.asset_cache.query(id, limit, **attributes)

    def on_load(self, *hooks: OnLoad[Asset]):
        self.hooks.on_load(hooks)


@dataclass
class CatalogsApiClient:
    humans: AssetCatalog[Human]
    hair: AssetCatalog[Hair]
    eyes: AssetCatalog[Eyes]
    eyebrows: AssetCatalog[Hair]
    beards: AssetCatalog[Hair]
    glasses: AssetCatalog[Glasses]
    masks: AssetCatalog[Mask]
    backgrounds: AssetCatalog[Background]

    def __post_init__(self):
        pretty_rich.install()
