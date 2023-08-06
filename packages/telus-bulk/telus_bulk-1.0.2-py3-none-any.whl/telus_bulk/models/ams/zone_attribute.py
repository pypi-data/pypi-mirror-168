from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import Field


class ZoneAttributes(CamelModel):
    coid: Optional[str] = Field(None, alias='COID')
    co_clli: Optional[str] = Field(None, alias='CO_CLLI')
    utc_offset: Optional[str] = Field(None, alias='UTC_OFFSET')
    time_zone_name: Optional[str] = Field(None, alias='TIME_ZONE_NAME')
    time_zone_abbreviations: Optional[str] = Field(
        None, alias='TIME_ZONE_ABBREVIATIONS'
    )
    time_zone_regions: Optional[str] = Field(None, alias='TIME_ZONE_REGIONS')
    e911_municipality: Optional[str] = Field(None, alias='E911_MUNICIPALITY')

