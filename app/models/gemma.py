from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Part(BaseModel):
    text: Optional[str] = None
    inline_data: Optional[Dict[str, Any]] = Field(None, alias="inlineData")

    def dict(self, *args, **kwargs):
        kwargs.pop("exclude_none", None)
        return super().dict(*args, exclude_none=True, **kwargs)

class Content(BaseModel):
    role: str
    parts: List[Part]

class GemmaPayload(BaseModel):
    contents: List[Content]

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs.update({"by_alias": True, "exclude_none": True})
        return super().dict(**kwargs)
