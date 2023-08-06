import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List

from datagen.api.datapoint.assets import (
    Human,
    Camera,
    Background,
    Light,
    Glasses,
    Mask,
    HumanDatapoint,
    DataRequest,
)
from datagen.api.datapoint.builder import HumanDatapointRequestBuilder, DatapointRequestDirector

DEFAULT_DATAPOINT_REQUESTS_JSON_NAME = "datagen_data_request.json"


@dataclass
class DatapointApiClient:
    _request_director: DatapointRequestDirector = field(default_factory=DatapointRequestDirector)

    def create_datapoint(
        self,
        human: Human,
        camera: Camera,
        glasses: Optional[Glasses] = None,
        mask: Optional[Mask] = None,
        background: Optional[Background] = None,
        lights: Optional[List[Light]] = None,
    ) -> HumanDatapoint:
        self._request_director.builder = HumanDatapointRequestBuilder(human, camera, glasses, mask, background, lights)
        return self._request_director.build_datapoint()

    def load(self, path: str) -> DataRequest:
        path_ = self._get_dump_path(path)
        if not path_.parent.exists():
            raise FileNotFoundError(f"json file does not exist, cannot load data request")
        return DataRequest.parse_file(path_)

    def dump(self, request: DataRequest, path: Optional[str] = None) -> None:
        data_request_copy = DataRequest(datapoints=[self._copy_predump(dp) for dp in request.datapoints])
        path_ = self._get_dump_path(path)
        path_.write_text(json.dumps(data_request_copy.dict(), indent=3, sort_keys=True))
        print(
            f"Data request was successfully dumped to path '{str(path_.absolute())}' " +
            f"({len(request.datapoints)} datapoints total)."""
        )

    def _get_dump_path(self, path: Optional[str]) -> Path:
        if path is None:
            path_ = Path.cwd().joinpath(DEFAULT_DATAPOINT_REQUESTS_JSON_NAME)
        else:
            path_ = Path(path)
        if not path_.parent.exists():
            raise FileNotFoundError(f"{path_.parent} folder does not exist, cannot dump requests")
        path_.touch()
        return path_

    def _copy_predump(self, req: HumanDatapoint) -> HumanDatapoint:
        self._request_director.builder = HumanDatapointRequestBuilder(
            human=req.human,
            camera=req.camera,
            glasses=req.accessories.glasses,
            mask=req.accessories.mask,
            background=req.background,
            lights=req.lights,
            remove_attributes=True,  # Attributes are not part of the request json and therefore shouldn't be dumped.
        )
        return self._request_director.build_datapoint()
