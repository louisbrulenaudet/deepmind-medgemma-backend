import httpx
import json
from fastapi import APIRouter, HTTPException, Request, Response
from app.models.gemma import GemmaPayload, Content, Part
from app.core.api_request import api_request
from pydantic import BaseModel
from starlette.responses import JSONResponse

router = APIRouter(tags=["gemma-web-search"])

class GemmaWebSearchRequest(BaseModel):
    prompt: str
    context: str

@router.post("/gemma-web-search")
async def gemma_web_search(request: GemmaWebSearchRequest, http_request: Request) -> Response:
    """
    Take a prompt and context, generate a search query with Gemma,
    and then call the /webscraper endpoint to perform a web search and scrape the results.
    """
    # 1. Generate search query with Gemma
    gemma_prompt = f"Based on the following prompt and context, generate a concise and effective web search query. The query should be no more than 10 words. Return only the search query and nothing else.\n\nPrompt: {request.prompt}\n\nContext: {request.context}"
    
    payload = GemmaPayload(
        contents=[
            Content(
                role="user",
                parts=[Part(text=gemma_prompt, inlineData=None)]
            )
        ]
    )

    try:
        gemma_response = await api_request(payload, model="gemini-1.5-flash")
        if gemma_response.get("status") != "success":
            error_message = gemma_response.get("error_message", "Unknown error from api_request")
            raise HTTPException(status_code=500, detail=f"Error from Gemma API: {error_message}")

        search_query = gemma_response.get("data", "").strip()
        if not search_query:
            raise HTTPException(status_code=500, detail="Empty search query received from Gemma")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating search query with Gemma: {e}")

    # 2. Call the /webscraper endpoint
    async with httpx.AsyncClient() as client:
        webscraper_url = http_request.url_for("webscraper")
        try:
            response = await client.post(str(webscraper_url), json={"query": search_query})
            response.raise_for_status()
            webscraper_data = response.json()
            
            # Format the web scraper data for the LLM
            search_results_text = ""
            for i, result in enumerate(webscraper_data.get("data", [])):
                search_results_text += f"Result {i+1}:\n"
                search_results_text += f"  Link: {result.get('link', 'N/A')}\n"
                search_results_text += f"  Snippet: {result.get('snippet', 'N/A')}\n\n"

            # Generate a summary with Gemma
            summary_prompt = f"""Based on the following web search results, provide a comprehensive answer to the user's original prompt. Synthesize the information from the different sources into a coherent response.

Original Prompt: {request.prompt}
Search Query: {search_query}

Search Results:
---
{search_results_text}
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
                final_response = {
                    "search_query": search_query,
                    "data": webscraper_data.get("data", [])
                }
                return Response(content=json.dumps(final_response, indent=4), media_type="text/plain")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from webscraper service: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Could not connect to webscraper service: {e}")
