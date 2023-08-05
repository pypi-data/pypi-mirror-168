from pydantic import Field

from datagen.api.datapoint.assets.base import DatapointRequestAsset
from datagen.api.datapoint.assets.types import FrameColor, LensColor, GlassesPosition
from datagen.config.config import settings

glasses = settings.assets.glasses


class Glasses(DatapointRequestAsset):
    id: str = Field(title="Glasses ID", description="Alphanumeric ID of the glasses")
    frame_color: FrameColor = Field(default=FrameColor[glasses.frame_color.default])
    frame_metalness: float = Field(
        title="Frame metalness",
        description="The higher the value, the more metallic (conductive) the frame is.\nIn real life items are "
        "either dielectric or conductive (0 or 1 metallic). Never are in between.",
        default=glasses.frame_metalness.default,
        ge=glasses.frame_metalness.min,
        le=glasses.frame_metalness.max,
    )
    lens_color: LensColor = Field(default=LensColor[glasses.lens_color.default])
    lens_reflectivity: float = Field(
        title="Lens reflectivity",
        description="The higher the value, the more reflective the lens are",
        default=glasses.lens_reflectivity.default,
        ge=glasses.lens_reflectivity.min,
        le=glasses.lens_reflectivity.max,
    )
    lens_transparency: float = Field(
        title="Lens transparency",
        description="The higher the value, the more transparent the lens are",
        default=glasses.lens_transparency.default,
        ge=glasses.lens_transparency.min,
        le=glasses.lens_transparency.max,
    )
    position: GlassesPosition = Field(default=GlassesPosition[glasses.position.default])
