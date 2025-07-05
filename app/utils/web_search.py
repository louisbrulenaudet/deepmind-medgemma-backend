from googleapiclient.discovery import build
from app.core.config import settings

__all__: list[str] = ["search"]


async def search(query: str, **kwargs) -> list[dict]:
    """
    Perform a web search using Google Custom Search API.

    Args:
        query: The query to search for.

    Returns:
        A list of search results.
    """
    service = build("customsearch", "v1", developerKey=settings.api_key)
    res = (
        service.cse()
        .list(
            q=query,
            cx=settings.google_cse_id,
            **kwargs,
        )
        .execute()
    )
    return res.get("items", [])