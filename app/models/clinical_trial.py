from pydantic import BaseModel, Field

__all__: list[str] = ["ClinicalTrialRequest"]


class ClinicalTrialRequest(BaseModel):
    query: str = Field(
        ...,
        description="The query string to search for clinical trials.",
    )
