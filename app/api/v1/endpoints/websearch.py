from aiocache import cached
from fastapi import APIRouter

from app.models.websearch import WebSearchRequest

# from app.core.config import settings

router = APIRouter(tags=["sync"])


@router.post(
    "/websearch",
)
@cached(ttl=60)
async def websearch(request: WebSearchRequest) -> dict:
    return {"data": "Placeholder for web search response"}
