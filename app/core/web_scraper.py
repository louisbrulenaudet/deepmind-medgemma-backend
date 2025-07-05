import httpx
from bs4 import BeautifulSoup

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
    return text
