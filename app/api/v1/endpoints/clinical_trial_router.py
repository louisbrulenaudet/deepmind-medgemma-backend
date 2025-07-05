from aiocache import cached
from fastapi import APIRouter

from app.models.clinical_trial import ClinicalTrialRequest

# from app.core.config import settings

router = APIRouter(tags=["sync"])


@router.post(
    "/trial",
    tags=["completion", "llm", "sync", "model", "text"],
    description="Endpoint to generate text completions for a given input using a registered model.",
)
@cached(ttl=60)
async def completion(request: ClinicalTrialRequest) -> dict:
    return {"data": "Placeholder for completion response"}
