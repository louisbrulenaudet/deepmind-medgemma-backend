from fastapi import APIRouter, HTTPException
from app.core.web_scraper import webscraper
from pydantic import BaseModel

router = APIRouter(tags=["web-scraper"])

class WebScraperRequest(BaseModel):
    query: str

@router.post("/web-scraper")
async def web_scraper_endpoint(request: WebScraperRequest):
    """
    Take a query, perform a web search and scrape the results.
    """
    try:
        return await webscraper(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during web scraping: {e}")
