from dataclasses import dataclass
from typing import Any

from IPython.core.display import display

from datagen.components import SourcesRepository
from datagen.components.dataset import Dataset, DatasetConfig

DEFAULT_DATASET_CONFIG = DatasetConfig(imaging_library="opencv")


@dataclass
class Datagen:
    def load(self, *dataset_sources: str, dataset_config: DatasetConfig = DEFAULT_DATASET_CONFIG) -> Dataset:
        sources_repo = SourcesRepository(dataset_sources)
        return Dataset(sources_repo=sources_repo, config=dataset_config)

    def explain(self, *explainables: Any) -> None:
        for e in explainables:
            try:
                display(e.get_explanation())
            except AttributeError:
                raise RuntimeError(f"Could not explain {e}")
