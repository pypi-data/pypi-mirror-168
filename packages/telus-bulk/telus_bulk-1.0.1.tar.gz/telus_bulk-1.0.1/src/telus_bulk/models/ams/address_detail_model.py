from typing import Any, List, Dict, Optional, Literal

from fastapi_camelcase import CamelModel
from pydantic import Field

from telus_bulk.models.ams.coordinate import Coordinate
from telus_bulk.models.ams.e911_address import E911Address
from telus_bulk.models.ams.fms_address import FmsAddress
from telus_bulk.models.ams.reference_id import ReferenceId
from telus_bulk.models.ams.reference_ids import ReferenceIds
from telus_bulk.models.ams.zone_info_item import ZoneInfoItem
from telus_bulk.models.worker_job.place import PlaceAMS


class AddressDetailModel(CamelModel):
    address_id: str
    address_type: str
    reference_id: ReferenceId
    reference_ids: ReferenceIds
    unit: Any
    floor: Any
    street_number_prefix: Any
    street_number: str
    street_number_suffix: Any
    dir_prefix: Any
    street_type_prefix: Any
    street_name: str
    street_type_suffix: Any
    dir_suffix: Any
    city: str
    province: str
    postal_code: Optional[str] = Field(default="N/A")
    country: Optional[Literal["USA", "CAN"]] = Field(default="CAN")
    coid: str
    serviceable: str
    serviceable_code: str
    building_type: str
    premise_count_flag: Any
    premise_count_date: Any
    postal_code_updt_ts: Any
    res_line_count: str
    bus_line_count: str
    mdu_sfu_count: str
    project_sub_type: Any
    first_nation_ind: str
    exception_code: Any
    nap_addr_assoc: Any
    coordinate: Coordinate
    zone_info: List[ZoneInfoItem]
    fms_address: FmsAddress
    e911_address: E911Address
    tag: List
    location_comments: Dict[str, Any]

    def to_csq_item(self) -> PlaceAMS:
        return PlaceAMS(
            id=self.address_id,
            city=self.city,
            country=self.country,
            postcode=self.postal_code,
            state_or_province=self.province,
            street_dir=self.dir_prefix,
            street_name=self.street_name,
            street_nr=self.street_number,
            street_type=self.street_type_prefix,
            floor=self.floor,
            unit=self.unit,
            address_type=self.address_type,
            coordinate=self.coordinate,
        )
