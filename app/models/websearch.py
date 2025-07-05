from pydantic import BaseModel, Field

__all__: list[str] = ["WebSearchRequest"]


class WebSearchRequest(BaseModel):
    query: str = Field(
        ...,
        description="The query string to search for web content.",
    )
