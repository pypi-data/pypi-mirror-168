from typing import Optional

from pydantic import BaseModel  # noqa: F401


class CredentialsResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


CredentialsResponse.update_forward_refs()