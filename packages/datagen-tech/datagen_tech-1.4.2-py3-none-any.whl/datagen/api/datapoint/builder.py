import abc
from dataclasses import dataclass, field
from typing import Optional, Union, TypeVar, List

from pydantic import BaseModel

from datagen.api.datapoint.assets import (
    Human,
    Camera,
    Glasses,
    Mask,
    Background,
    Light,
    HumanDatapoint,
    Accessories,
)
Asset = TypeVar("Asset")


@dataclass
class HumanDatapointRequestBuilder:
    human: Human
    camera: Camera
    glasses: Optional[Glasses]
    mask: Optional[Mask]
    background: Optional[Background]
    lights: Optional[List[Light]]
    remove_attributes: bool = False

    def get_basic_datapoint(self) -> HumanDatapoint:
        return HumanDatapoint(human=self._deepcopy_human(), camera=self._deepcopy(self.camera))

    def _deepcopy_human(self) -> Human:
        human = self._deepcopy(self.human)
        if self.remove_attributes:
            self._remove_nested_attributes(human)
        return human

    def _remove_nested_attributes(self, human: Human) -> None:
        head = human.head
        self._remove_attributes(head)
        self._remove_attributes(head.hair)
        self._remove_attributes(head.eyes)
        self._remove_attributes(head.eyebrows)
        self._remove_attributes(head.facial_hair)

    def _remove_attributes(self, asset: BaseModel) -> None:
        if asset and hasattr(asset, "attributes"):
            delattr(asset, "attributes")

    def get_accessories(self) -> Accessories:
        accessories = Accessories()
        if self.glasses is not None:
            accessories.glasses = self._deepcopy(self.glasses)
        if self.mask is not None:
            accessories.mask = self._deepcopy(self.mask)
        return accessories

    def get_background(self) -> Union[Background, None]:
        if self.background is not None:
            return self._deepcopy(self.background)
        else:
            return None

    def get_lights(self) -> Union[List[Light], None]:
        if self.lights is not None and len(self.lights) > 0:
            return [self._deepcopy(l) for l in self.lights]
        else:
            return None

    def _deepcopy(self, asset: Asset) -> Asset:
        if self.remove_attributes:
            return asset.copy(deep=True, exclude={"attributes"})
        else:
            return asset.copy(deep=True)

@dataclass
class DatapointRequestDirector:
    builder: HumanDatapointRequestBuilder = field(init=False)

    def build_datapoint(self) -> HumanDatapoint:
        datapoint = self.builder.get_basic_datapoint()
        datapoint.accessories = self.builder.get_accessories()
        datapoint.background = self.builder.get_background()
        datapoint.lights = self.builder.get_lights()
        return datapoint
