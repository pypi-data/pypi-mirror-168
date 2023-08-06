from pydantic import Field

from datagen.api.datapoint.assets.base import DatapointRequestAsset
from datagen.api.datapoint.assets.orientation.vector import Vector
from datagen.config.config import settings

eyes = settings.assets.eyes


class Gaze(DatapointRequestAsset):
    distance: float = Field(
        title="Look at distance",
        description="Distance from the actor to the point at which they are looking",
        default=eyes.target_of_gaze.distance.default,
        ge=eyes.target_of_gaze.distance.min,
    )
    direction: Vector = Field(
        default_factory=lambda: Vector(
            x=eyes.target_of_gaze.direction.x.default,
            y=eyes.target_of_gaze.direction.y.default,
            z=eyes.target_of_gaze.direction.z.default,
        )
    )


class Eyes(DatapointRequestAsset):
    id: str = Field(title="Eyes ID", description="String ID of the eyes")
    target_of_gaze: Gaze = Field(default_factory=Gaze)
    eyelid_closure: float = Field(
        title="Eyelid closure",
        description="The higher the value, the more closed the eye is",
        default=eyes.eyelid_closure.default,
        ge=eyes.eyelid_closure.min,
        le=eyes.eyelid_closure.max,
    )
