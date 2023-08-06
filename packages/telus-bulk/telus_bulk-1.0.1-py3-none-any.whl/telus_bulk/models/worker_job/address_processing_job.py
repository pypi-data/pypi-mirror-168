from __future__ import annotations

from typing import Union, Optional, List

from fastapi_camelcase import CamelModel
from telus_bulk.models.tmf_645.characteristic import Characteristic
from telus_bulk.models.worker_job.place import Place, PlaceAMS
from telus_bulk.models.worker_job.service_specification import ServiceSpecification
from telus_bulk.models.product_type import ProductType


class AddressProcessingJob(CamelModel):
    csq_id: str
    instant_sync_qualification: bool
    provide_alternative: bool
    place: Union[PlaceAMS, Place]
    service_specification: ServiceSpecification
    service_characteristic: Optional[List[Characteristic]] = None

    def get_product_type(self):
        default_type = ProductType.nhp
        if self.service_specification is None:
            return default_type
        if self.service_specification.name == (
            "Off_Net_Unmanaged" or "off_net_unmanaged"
        ):
            return ProductType.nhp
        elif self.service_specification.name == (
            "Off_Net_Managed" or "off_net_managed"
        ):
            return ProductType.fib
        return default_type
