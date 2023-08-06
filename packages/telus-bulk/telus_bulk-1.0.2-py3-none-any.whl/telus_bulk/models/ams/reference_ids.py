from fastapi_camelcase import CamelModel
from pydantic import Field


class ReferenceIds(CamelModel):
    lpds_id: str = Field(..., alias='LPDS_ID')
    fms_id: str = Field(..., alias='FMS_ID')