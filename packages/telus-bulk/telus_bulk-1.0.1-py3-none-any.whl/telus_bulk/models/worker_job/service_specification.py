from __future__ import annotations
from typing import Optional
from fastapi_camelcase import CamelModel
from pydantic import Field


class ServiceSpecification(CamelModel):
    id: Optional[str] = Field(default=None)
    href: Optional[str] = Field(default=None)
    name: str
    version: Optional[str] = Field(default=None)
    _type: Optional[str] = Field(default="ServiceSpecification", alias="@type")
