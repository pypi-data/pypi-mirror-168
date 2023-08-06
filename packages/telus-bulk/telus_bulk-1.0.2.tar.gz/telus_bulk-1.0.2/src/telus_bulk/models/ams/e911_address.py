from typing import Any, Optional

from fastapi_camelcase import CamelModel


class E911Address(CamelModel):
    unit: Optional[Any]
    house_number: Optional[str]
    house_suffix: Optional[Any]
    street_name: Optional[str]
    street_type: Optional[Any]
    street_vector_prefix: Optional[Any]
    street_vector_suffix: Optional[Any]
    municipality: Optional[str]
    province: Optional[str]
    postal_code: Optional[str]
    e911_clli: Optional[str]
    esz_number: Optional[str]
