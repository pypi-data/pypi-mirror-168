from typing import Any

from fastapi_camelcase import CamelModel
from pydantic import Field


class Coordinate(CamelModel):
    srs_code: str = Field(..., alias='srsCode')
    latitude: float
    longitude: float
    location_accuracy_score: str = Field(..., alias='locationAccuracyScore')
    location_provider: Any = Field(..., alias='locationProvider')
    location_update_ts: str = Field(..., alias='locationUpdateTs')