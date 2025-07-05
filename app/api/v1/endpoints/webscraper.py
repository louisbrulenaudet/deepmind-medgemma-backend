import asyncio
from fastapi import APIRouter
from app.models.websearch import WebSearchRequest
from app.utils.web_search import search
from app.core.web_scraper import scrape_url

router = APIRouter(tags=["web-scraper"])

@router.post("/webscraper")
async def webscraper(request: WebSearchRequest) -> dict:
    """
    Perform a web search and scrape the content of the search results.
    """
    search_results = await search(request.query)

    async def scrape_and_add(result: dict):
        url = result.get("link")
        if url:
            scraped_content = await scrape_url(url)
            result["scraped_content"] = scraped_content

    await asyncio.gather(*(scrape_and_add(result) for result in search_results))

    return {"data": search_results}
