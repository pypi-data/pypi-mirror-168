from typing import Optional

from pydantic import BaseModel  # noqa: F401


class ExampleModel(BaseModel):
    id: Optional[str] = None
    msg: str = "Hello World!"


ExampleModel.update_forward_refs()
