from datagen.api.catalog.hooks.impl import OnLoad
from datagen.api.datapoint.assets.human.eyes import Eyes


class SetEyeColorFromAttributes(OnLoad[Eyes]):
    def __call__(self, asset: Eyes) -> None:
        ...
