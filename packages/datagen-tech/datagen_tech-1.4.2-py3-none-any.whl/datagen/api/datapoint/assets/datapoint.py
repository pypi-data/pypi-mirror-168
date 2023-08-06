from typing import Optional, List

from pydantic import validator

from datagen.api.datapoint.assets.accessories.accessories import Accessories
from datagen.api.datapoint.assets.base import DatapointRequestAsset
from datagen.api.datapoint.assets.environment.camera import Camera
from datagen.api.datapoint.assets.environment.background import Background
from datagen.api.datapoint.assets.environment.light import Light
from datagen.api.datapoint.assets.human.human import Human
from datagen.api.datapoint.assets.types import Wavelength


class HumanDatapoint(DatapointRequestAsset):
    human: Human
    camera: Camera
    accessories: Optional[Accessories]
    background: Optional[Background]
    lights: Optional[List[Light]]

    @validator("lights", always=True)
    def lights_and_not_nir_mutually_exclusive(cls, lights, values) -> List[Light]:
        has_lights = lights is not None and len(lights) > 0
        if has_lights and not cls._is_set_to_nir(values["camera"]):
            raise ValueError("Lights are only relevant if the camera is using 'nir' wavelength")
        return lights

    @validator("background", always=True)
    def background_and_nir_mutually_exclusive(cls, background, values) -> Background:
        if background is not None and cls._is_set_to_nir(values["camera"]):
            raise ValueError("Background is only relevant if the camera is not using 'nir' wavelength")
        return background

    @staticmethod
    def _is_set_to_nir(camera: Camera) -> bool:
        return camera.intrinsic_params.wavelength == Wavelength.NIR


class DataRequest(DatapointRequestAsset):
    datapoints: List[HumanDatapoint]
