import json
from pathlib import Path
from dependency_injector import containers, providers

from datagen.api.catalog.hooks.eyes_color import SetEyeColorFromAttributes
from datagen.api.catalog.hooks.impl import AssetLoadingHooks
from datagen.api.catalog.impl import AssetCatalog, CatalogsApiClient
from datagen.api.catalog.cache import InMemAssetCache
from datagen.api.catalog.attributes import (
    GlassesAttributes,
    HairAttributes,
    BackgroundAttributes,
    MaskAttributes,
    HumanAttributes,
    EyebrowsAttributes,
    EyesAttributes,
    BeardAttributes,
)
from datagen.api.datapoint.assets import Human, Eyes, Hair, Background
from datagen.api.datapoint.assets import Mask, Glasses


def _create_human(id: str) -> Human:
    with open(Path(__file__).parent.joinpath("human_templates", "neutral.json")) as f:
        human_dict = json.load(f)
        human_dict["id"] = id
    return Human.parse_obj(human_dict)


class DatapointRequestAssetsContainer(containers.DeclarativeContainer):
    human = providers.Callable(_create_human)

    eyes = providers.Factory(Eyes)

    glasses = providers.Factory(Glasses)

    hair = providers.Factory(Hair)

    mask = providers.Factory(Mask)

    background = providers.Factory(Background)


def _get_attributes_provider(attributes_dataclass_type: type) -> providers.Provider:
    return providers.Callable(attributes_dataclass_type.Schema().load).provider


class CatalogsApiContainer(containers.DeclarativeContainer):
    _assets = providers.Container(DatapointRequestAssetsContainer)

    humans = providers.Singleton(
        AssetCatalog,
        asset_provider=_assets.human.provider,
        asset_cache=providers.Singleton(
            InMemAssetCache,
            attributes_provider=_get_attributes_provider(HumanAttributes),
            cache_file_name="humans.json",
        ),
    )

    eyes = providers.Singleton(
        AssetCatalog,
        asset_provider=_assets.eyes.provider,
        asset_cache=providers.Singleton(
            InMemAssetCache,
            attributes_provider=_get_attributes_provider(EyesAttributes),
            cache_file_name="eyes.json",
        ),
        hooks=providers.Singleton(
            AssetLoadingHooks, hooks=providers.List(providers.Singleton(SetEyeColorFromAttributes))
        ),
    )

    hair = providers.Singleton(
        AssetCatalog,
        asset_provider=_assets.hair.provider,
        asset_cache=providers.Singleton(
            InMemAssetCache,
            attributes_provider=_get_attributes_provider(HairAttributes),
            cache_file_name="hair.json",
        ),
    )

    eyebrows = providers.Singleton(
        AssetCatalog,
        asset_provider=_assets.hair.provider,
        asset_cache=providers.Singleton(
            InMemAssetCache,
            attributes_provider=_get_attributes_provider(EyebrowsAttributes),
            cache_file_name="eyebrows.json",
        ),
    )

    beards = providers.Singleton(
        AssetCatalog,
        asset_provider=_assets.hair.provider,
        asset_cache=providers.Singleton(
            InMemAssetCache,
            attributes_provider=_get_attributes_provider(BeardAttributes),
            cache_file_name="beards.json",
        ),
    )

    glasses = providers.Singleton(
        AssetCatalog,
        asset_provider=_assets.glasses.provider,
        asset_cache=providers.Singleton(
            InMemAssetCache,
            attributes_provider=_get_attributes_provider(GlassesAttributes),
            cache_file_name="glasses.json",
        ),
    )

    masks = providers.Singleton(
        AssetCatalog,
        asset_provider=_assets.mask.provider,
        asset_cache=providers.Singleton(
            InMemAssetCache,
            attributes_provider=_get_attributes_provider(MaskAttributes),
            cache_file_name="masks.json",
        ),
    )

    backgrounds = providers.Singleton(
        AssetCatalog,
        asset_provider=_assets.background.provider,
        asset_cache=providers.Singleton(
            InMemAssetCache,
            attributes_provider=_get_attributes_provider(BackgroundAttributes),
            cache_file_name="backgrounds.json",
        ),
    )

    catalogs_api = providers.Singleton(
        CatalogsApiClient,
        humans=humans,
        hair=hair,
        eyes=eyes,
        eyebrows=eyebrows,
        beards=beards,
        glasses=glasses,
        backgrounds=backgrounds,
        masks=masks,
    )
