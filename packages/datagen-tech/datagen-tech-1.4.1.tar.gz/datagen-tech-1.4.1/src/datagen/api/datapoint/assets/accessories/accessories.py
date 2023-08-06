from typing import Optional

from pydantic import validator

from datagen.api.datapoint.assets.accessories.glasses import Glasses
from datagen.api.datapoint.assets.accessories.mask import Mask
from datagen.api.datapoint.assets.base import DatapointRequestAsset


class Accessories(DatapointRequestAsset):
    glasses: Optional[Glasses]
    mask: Optional[Mask]

    @validator("mask", always=True)
    def glasses_and_masks_mutually_exclusive(cls, mask, values) -> Mask:
        if mask and "glasses" in values and values["glasses"]:
            raise ValueError("Glasses and masks are mutually exclusive")
        return mask
