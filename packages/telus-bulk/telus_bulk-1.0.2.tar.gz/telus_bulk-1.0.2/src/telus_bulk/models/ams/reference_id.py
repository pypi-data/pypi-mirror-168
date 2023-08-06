from typing import Any

from fastapi_camelcase import CamelModel
from pydantic import Field


class ReferenceId(CamelModel):
    fms_id: str = Field(..., alias='fmsId')
    loc_building_id: str = Field(..., alias='locBuildingId')
    loc_grp_id: Any = Field(..., alias='locGrpId')