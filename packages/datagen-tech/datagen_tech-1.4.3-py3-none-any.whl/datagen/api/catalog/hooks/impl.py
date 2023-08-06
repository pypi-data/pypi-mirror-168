import abc
from dataclasses import dataclass, field
from typing import List, Generic, TypeVar, Tuple

Asset = TypeVar("Asset")


@dataclass
class OnLoad(abc.ABC, Generic[Asset]):
    @abc.abstractmethod
    def __call__(self, asset: Asset) -> None:
        ...


@dataclass
class AssetLoadingHooks(Generic[Asset]):
    hooks: List[OnLoad[Asset]] = field(default_factory=list)

    def apply_all(self, asset: Asset) -> None:
        for h in self.hooks:
            h(asset)

    def on_load(self, hooks: Tuple[OnLoad[Asset]]) -> None:
        self.hooks.extend(hooks)
