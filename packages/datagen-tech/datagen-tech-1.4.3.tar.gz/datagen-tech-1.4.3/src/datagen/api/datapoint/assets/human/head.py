from typing import Optional

from pydantic import Field

from datagen.api.datapoint.assets.base import DatapointRequestAsset
from datagen.api.datapoint.assets.human.expression import Expression
from datagen.api.datapoint.assets.human.eyes import Eyes
from datagen.api.datapoint.assets.human.hair import Hair
from datagen.api.datapoint.assets.orientation.rotation import HeadRotation
from datagen.api.datapoint.assets.orientation.point import Point
from datagen.config.config import settings

head = settings.assets.head


class Head(DatapointRequestAsset):
    eyes: Eyes
    facial_hair: Optional[Hair]
    hair: Optional[Hair]
    eyebrows: Optional[Hair]
    location: Point = Field(
        default_factory=lambda: Point(x=head.location.x.default, y=head.location.y.default, z=head.location.z.default)
    )
    rotation: HeadRotation = Field(default_factory=HeadRotation)
    expression: Expression = Field(default_factory=Expression)
