from pydantic import Field

from datagen.api.datapoint.assets.base import DatapointRequestAsset
from datagen.api.datapoint.assets.types import MaskPosition, MaskTexture, MaskColor
from datagen.config.config import settings

mask = settings.assets.mask


class Mask(DatapointRequestAsset):
    id: str = Field(title="Mask ID", description="Alphanumeric ID of the mask")
    color: MaskColor = Field(default=MaskColor[mask.color.default])
    texture: MaskTexture = Field(default=MaskTexture[mask.texture.default])
    roughness: float = Field(
        title="Roughness",
        description="The higher the value, the more matte and less reflective the mask is",
        default=mask.roughness.default,
        ge=mask.roughness.min,
        le=mask.roughness.max,
    )
    position: MaskPosition = Field(default=MaskPosition[mask.position.default])
