from typing import Any

from pydantic import BaseModel, Field


class Part(BaseModel):
    text: str | None = None
    inline_data: dict[str, Any] | None = Field(None, alias="inlineData")

    def dict(self, *args: object, **kwargs: object) -> dict[str, Any]:
        kwargs.pop("exclude_none", None)
        return super().dict(*args, exclude_none=True, **kwargs)

class Content(BaseModel):
    role: str
    parts: list[Part]


class GemmaPayload(BaseModel):
    contents: list[Content]

    def dict(self, **kwargs: object) -> dict[str, Any]:
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().dict(**kwargs)
