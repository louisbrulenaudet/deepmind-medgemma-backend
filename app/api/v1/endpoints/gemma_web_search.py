from fastapi import APIRouter, HTTPException
from app.models.gemma import GemmaPayload, Content, Part
from app.core.api_request import api_request
from pydantic import BaseModel
from starlette.responses import JSONResponse
from app.core.web_scraper import webscraper

router = APIRouter(tags=["gemma-web-search"])

class GemmaWebSearchRequest(BaseModel):
    prompt: str
    context: str

@router.post("/gemma-web-search")
async def gemma_web_search(request: GemmaWebSearchRequest) -> JSONResponse:
    """
    Take a prompt and context, generate a search query with Gemma,
    and then call the webscraper function to perform a web search and scrape the results.
    """
    # 1. Generate search query with Gemma
    gemma_prompt = f"Based on the following prompt and context, generate a concise and effective web search query. The query should be no more than 10 words. Return only the search query and nothing else.\n\nPrompt: {request.prompt}\n\nContext: {request.context}"
    
    payload = GemmaPayload(
        contents=[
            Content(
                role="user",
                parts=[Part(text=gemma_prompt)]
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

    # 2. Call the webscraper function
    try:
        webscraper_data = await webscraper(search_query)
        
        # Add the search query to the final response
        final_response = {
            "search_query": search_query,
            "data": webscraper_data.get("data", [])
        }
        return JSONResponse(content=final_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during web scraping: {e}")
