from pydantic import BaseModel, Field

__all__: list[str] = ["ClinicalTrialRequest"]


class ClinicalTrialRequest(BaseModel):
    n_results: int = Field(
        default=3,
        ge=1,
        le=100,
        description="The number of results to return. Must be between 1 and 100.",
    )
    query: str = Field(
        ...,
        description="The query string to search for clinical trials.",
    )


class ClinicalTrialResult(BaseModel):
    id: str
    document: str
    metadata: dict
    distance: float | None = None
    uri: str | None = None


class ClinicalTrialResults(BaseModel):
    results: list[ClinicalTrialResult] = Field(
        default_factory=list,
        description="List of clinical trial results.",
    )
