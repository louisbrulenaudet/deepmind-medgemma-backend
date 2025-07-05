import json
from aiocache import cached
from fastapi import APIRouter, Response
from app.core.api_request import api_request
from app.models.gemma import Content, GemmaPayload, Part

from app.core.clinical_trial import ClinicalTrialRetriever
from app.models.clinical_trial import ClinicalTrialRequest

router = APIRouter(tags=["sync"])


@router.post(
    "/trial",
    tags=["completion", "llm", "sync", "model", "text"],
    description="Endpoint to generate text completions for a given input using a registered model.",
)
@cached(ttl=60)
async def completion(request: ClinicalTrialRequest) -> Response:
    """Generate clinical trial results based on the provided query and number of results.

    Example query :
    {
        "query": "What are the latest clinical trials for diabetes?",
        "n_results": 5
    }

    Args:
        request (ClinicalTrialRequest): The request containing the query and number of results.

    Returns:
        Response: A FastAPI response object containing the clinical trial results as a raw string.
    """
    retriever = ClinicalTrialRetriever()
    results = retriever(query=request.query, n_results=request.n_results)
    
    if not results.results:
        return Response(content="No clinical trials found for the given query.", media_type="text/plain")

    # Format the clinical trial data for the LLM
    trial_results_text = ""
    for i, result in enumerate(results.results):
        trial_results_text += f"Trial {i+1}:\n"
        trial_results_text += f"  Official Title: {result.metadata.get('official_title', 'N/A')}\n"
        trial_results_text += f"  NCT ID: {result.metadata.get('nct_id', 'N/A')}\n"
        trial_results_text += f"  Brief Summary: {result.metadata.get('brief_summary', 'N/A')}\n\n"

    # Generate a summary with Gemma
    summary_prompt = f"""Based on the following clinical trial results, provide a comprehensive answer to the user's original query. Synthesize the information from the different sources into a coherent response.

Original Query: {request.query}

Clinical Trial Results:
---
{trial_results_text}
---

Comprehensive Answer:
"""

    summary_payload = GemmaPayload(
        contents=[
            Content(
                role="user",
                parts=[Part(text=summary_prompt, inlineData=None)]
            )
        ]
    )

    summary_response = await api_request(summary_payload, model="gemini-1.5-flash")

    if summary_response.get("status") == "success" and summary_response.get("data"):
        return Response(content=summary_response["data"], media_type="text/plain")
    else:
        # Fallback to returning the JSON if summary fails
        results_str = json.dumps(results.model_dump(exclude_none=True), indent=4)
        return Response(content=results_str, media_type="text/plain")
