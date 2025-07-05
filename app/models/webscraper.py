from pydantic import BaseModel

class WebScraperRequest(BaseModel):
    query: str
