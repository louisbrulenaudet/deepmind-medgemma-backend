from pydantic import BaseModel


class ScanRequest(BaseModel):
    image_base64: str
