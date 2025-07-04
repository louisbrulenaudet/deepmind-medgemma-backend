from typing import Any

from pydantic import BaseModel, Field

__all__: list[str] = [
    "Completion",
]


class Completion(BaseModel):
    data: str | list[Any] | dict[str, Any] | None = Field(
        default=None,
        description="The generated content from the model, which can be text or structured data.",
    )
