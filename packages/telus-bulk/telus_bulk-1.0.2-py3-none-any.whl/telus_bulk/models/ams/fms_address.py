from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field


class FmsAddress(CamelModel):
    sa_no: Optional[str] = Field(..., alias="saNo")
    resc_cd: Optional[str] = Field(..., alias="rescCd")
    sa_house: Optional[str] = Field(..., alias="saHouse")
    sa_street_name: Optional[str] = Field(..., alias="saStreetName")
    sa_city_province_code: Optional[str] = Field(..., alias="saCityProvinceCode")
    sa_postal_code: Optional[str] = Field(default="N/A", alias="saPostalCode")
    sa_clli_code: Optional[str] = Field(..., alias="saCLLICode")
    serv_coid: Optional[str] = Field(..., alias="servCoid")
    sa_clli_prov_cd: Optional[str] = Field(..., alias="saClliProvCd")
