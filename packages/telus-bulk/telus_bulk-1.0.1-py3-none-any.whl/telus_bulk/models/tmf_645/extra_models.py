# coding: utf-8

from fastapi_camelcase import CamelModel


class TokenModel(CamelModel):
    """Defines a token model."""

    sub: str
