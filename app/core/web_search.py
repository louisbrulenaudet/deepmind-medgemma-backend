from aiocache import cached
from app.utils.web_search import search


@cached(ttl=60)
async def websearch(query: str) -> dict:
    results = await search(query)
    return {"data": results}
