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
            if scraped_content:
                result["scraped_content"] = scraped_content

    await asyncio.gather(*(scrape_and_add(result) for result in search_results))

    # Filter out results without scraped content and format the output
    filtered_results = [
        {
            "snippet": result.get("snippet"),
            "link": result.get("link"),
            "scraped_content": result.get("scraped_content"),
        }
        for result in search_results
        if result.get("scraped_content")
    ]

    return {"data": filtered_results}
