from __future__ import annotations

from typing import Optional, Literal

from fastapi_camelcase import CamelModel
from pydantic import Field
from telus_bulk.models.ams.coordinate import Coordinate


class Place(CamelModel):
    id: str
    role: Optional[str] = None
    _type: str = Field(alias="@type", default="GeographicAddress")


class PlaceAMS(Place):
    city: Optional[str] = None
    country: Literal["USA", "CAN"] = "CAN"
    postcode: Optional[str] = None
    state_or_province: Optional[str] = None
    street_dir: Optional[str] = None
    street_name: Optional[str] = None
    street_nr: Optional[str] = None
    street_type: Optional[str] = None
    floor: Optional[str] = None
    unit: Optional[str] = None
    address_type: Optional[str] = None
    coordinate: Optional[Coordinate] = None
