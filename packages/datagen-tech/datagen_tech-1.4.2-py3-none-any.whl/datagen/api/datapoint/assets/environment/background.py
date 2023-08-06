from typing import Optional

from pydantic import Field

from datagen.api.datapoint.assets.base import DatapointRequestAsset
from datagen.config.config import settings

background = settings.assets.background


class Background(DatapointRequestAsset):
    id: Optional[str] = Field(title="HDRI ID", description="Alphanumeric ID of the HDRI")
    transparent: bool = Field(
        title="Transparent", description="Make the background transparent", default=background.transparency.default
    )
    rotation: float = Field(
        title="Rotation degree",
        description="The rotation degree of the background",
        default=background.rotation.default,
        ge=background.rotation.min,
        le=background.rotation.max,
    )
