from pydantic import BaseModel, Field

from datagen.config.config import settings

head = settings.assets.head


class HeadRotation(BaseModel):
    yaw: float = Field(
        title="Vertical / Yaw rotation",
        description="Yaw axis is directed towards the bottom of the object",
        default=head.rotation.yaw.default,
        ge=head.rotation.yaw.min,
        le=head.rotation.yaw.max,
    )
    roll: float = Field(
        title="Longitudinal / Roll rotation",
        description="Roll axis is directed towards the front of the object",
        default=head.rotation.roll.default,
        ge=head.rotation.roll.min,
        le=head.rotation.roll.max,
    )
    pitch: float = Field(
        title="Transverse / Pitch rotation",
        description="Pitch axis is directed to the right of the object",
        default=head.rotation.pitch.default,
        ge=head.rotation.pitch.min,
        le=head.rotation.pitch.max,
    )


camera = settings.assets.camera


class CameraRotation(BaseModel):
    yaw: float = Field(
        title="Vertical / Yaw rotation",
        description="Yaw axis is directed towards the bottom of the object",
        default=camera.rotation.yaw.default,
        ge=camera.rotation.yaw.min,
        le=camera.rotation.yaw.max,
    )
    roll: float = Field(
        title="Longitudinal / Roll rotation",
        description="Roll axis is directed towards the front of the object",
        default=camera.rotation.roll.default,
        ge=camera.rotation.roll.min,
        le=camera.rotation.roll.max,
    )
    pitch: float = Field(
        title="Transverse / Pitch rotation",
        description="Pitch axis is directed to the right of the object",
        default=camera.rotation.pitch.default,
        ge=camera.rotation.pitch.min,
        le=camera.rotation.pitch.max,
    )


light = settings.assets.light


class LightRotation(BaseModel):
    yaw: float = Field(
        title="Vertical / Yaw rotation",
        description="Yaw axis is directed towards the bottom of the object",
        default=light.rotation.yaw.default,
        ge=light.rotation.yaw.min,
        le=light.rotation.yaw.max,
    )
    roll: float = Field(
        title="Longitudinal / Roll rotation",
        description="Roll axis is directed towards the front of the object",
        default=light.rotation.roll.default,
        ge=light.rotation.roll.min,
        le=light.rotation.roll.max,
    )
    pitch: float = Field(
        title="Transverse / Pitch rotation",
        description="Pitch axis is directed to the right of the object",
        default=light.rotation.pitch.default,
        ge=light.rotation.pitch.min,
        le=light.rotation.pitch.max,
    )
