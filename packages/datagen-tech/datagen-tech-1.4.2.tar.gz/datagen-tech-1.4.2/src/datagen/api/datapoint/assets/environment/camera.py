from pydantic import Field

from datagen.config.config import settings
from datagen.api.datapoint.assets.base import DatapointRequestAsset
from datagen.api.datapoint.assets.types import Projection, Wavelength
from datagen.api.datapoint.assets.orientation.point import Point

from datagen.api.datapoint.assets.orientation.rotation import CameraRotation

camera = settings.assets.camera


class IntrinsicParams(DatapointRequestAsset):
    projection: Projection = Field(
        title="Camera type",
        description="Currently, only perspective camera is supported",
        default=Projection[camera.intrinsic.projection.default],
    )
    resolution_width: int = Field(
        title="Resolution width",
        description="Width resolution in pixels",
        default=camera.intrinsic.resolution_width.default,
        ge=camera.intrinsic.resolution_width.min,
        le=camera.intrinsic.resolution_width.max,
    )
    resolution_height: int = Field(
        title="Resolution height",
        description="Height resolution in pixels",
        default=camera.intrinsic.resolution_height.default,
        ge=camera.intrinsic.resolution_height.min,
        le=camera.intrinsic.resolution_height.max,
    )
    fov_horizontal: int = Field(
        title="Horizontal field of view",
        description="Horizontal angle of view",
        default=camera.intrinsic.fov_horizontal.default,
        ge=camera.intrinsic.fov_horizontal.min,
        le=camera.intrinsic.fov_horizontal.max,
    )
    fov_vertical: int = Field(
        title="Vertical field of view",
        description="Vertical angle of view",
        default=camera.intrinsic.fov_vertical.default,
        ge=camera.intrinsic.fov_vertical.min,
        le=camera.intrinsic.fov_vertical.max,
    )
    sensor_width: float = Field(
        title="Sensor width",
        description="Horizontal size of the sensor in millimeters",
        default=camera.intrinsic.sensor_width.default,
        # ge=intrinsic_settings.sensor_width.min,
        # le=intrinsic_settings.sensor_width.max,
    )
    wavelength: Wavelength = Wavelength[camera.intrinsic.wavelength.default]


class ExtrinsicParams(DatapointRequestAsset):
    location: Point = Field(
        default_factory=lambda: Point(x=camera.location.x, y=camera.location.y, z=camera.location.z)
    )
    rotation: CameraRotation = Field(default_factory=CameraRotation)


class Camera(DatapointRequestAsset):
    name: str = Field(title="Camera name", description="Name of the camera", default=camera.name)
    intrinsic_params: IntrinsicParams = Field(default_factory=IntrinsicParams)
    extrinsic_params: ExtrinsicParams = Field(default_factory=ExtrinsicParams)
