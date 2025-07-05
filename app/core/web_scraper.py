import httpx
from bs4 import BeautifulSoup
from app.core.config import settings

async def search(query: str) -> list[dict]:
    """
    Search the web for a query.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": settings.api_key,
        "cx": settings.google_cse_id,
        "q": query,
        "num": 5,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])

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

    soup = BeautifulSoup(response.text, "lxml")
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
