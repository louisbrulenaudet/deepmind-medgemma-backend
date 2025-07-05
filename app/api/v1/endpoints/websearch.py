from aiocache import cached
from fastapi import APIRouter

from app.models.websearch import WebSearchRequest
from app.utils.web_search import search

# from app.core.config import settings

router = APIRouter(tags=["sync"])


@router.post(
    "/websearch",
)
@cached(ttl=60)
async def websearch(request: WebSearchRequest) -> dict:
    print(request.query)
    results = await search(request.query)
    return {"data": results}
