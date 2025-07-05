from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Part(BaseModel):
    text: Optional[str] = None
    inline_data: Optional[Dict[str, Any]] = None

class Content(BaseModel):
    role: str
    parts: List[Part]

class GeminiPayload(BaseModel):
    contents: List[Content]
