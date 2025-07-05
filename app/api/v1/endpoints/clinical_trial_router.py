from aiocache import cached
from fastapi import APIRouter

from app.core.clinical_trial import ClinicalTrialRetriever
from app.models.clinical_trial import ClinicalTrialRequest

router = APIRouter(tags=["sync"])


@router.post(
    "/trial",
    tags=["completion", "llm", "sync", "model", "text"],
    description="Endpoint to generate text completions for a given input using a registered model.",
)
@cached(ttl=60)
async def completion(request: ClinicalTrialRequest) -> dict:
    """Generate clinical trial results based on the provided query and number of results.

    Example query :
    {
        "query": "What are the latest clinical trials for diabetes?",
        "n_results": 5
    }

    Args:
        request (ClinicalTrialRequest): The request containing the query and number of results.

    Returns:
        dict: A dictionary containing the clinical trial results.
    """
    retriever = ClinicalTrialRetriever()
    results = retriever(query=request.query, n_results=request.n_results)

    return {"data": results.model_dump(exclude_none=True)}
