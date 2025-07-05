import asyncio
import httpx
from bs4 import BeautifulSoup
from app.utils.web_search import search


async def scrape_url(url: str) -> str:
    """
    Scrape the content of a URL.

    Args:
        url: The URL to scrape.

    Returns:
        The text content of the URL.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get("content-type")
            if content_type and "text/html" not in content_type:
                return ""  # Not an HTML page

        except httpx.HTTPStatusError as e:
            return f"HTTP error occurred: {e}"
        except httpx.RequestError as e:
            return f"An error occurred while requesting {e.request.url!r}: {e}"

    parser = "lxml"
    if "xml" in content_type:
        parser = "lxml-xml"
    soup = BeautifulSoup(response.text, parser)
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # Get text
    text = soup.get_text()
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)
    
    # Limit character count
    return text[:1500]


async def webscraper(query: str) -> dict:
    """
    Perform a web search and scrape the content of the search results.
    """
    search_results = await search(query)

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
