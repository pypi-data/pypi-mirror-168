from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import Field

from telus_bulk.models.ams.zone_attribute import ZoneAttributes


class ZoneInfoItem(CamelModel):
    zone_type: str = Field(..., alias="zoneType")
    zone_name: str = Field(..., alias="zoneName")
    zone_attributes: Optional[ZoneAttributes] = Field(None, alias="zoneAttributes")
