import time

from aiocache import cached
from fastapi import APIRouter, File, HTTPException, UploadFile

from app._enums import ImageMimeTypes
from app.core.config import settings

router = APIRouter(tags=["sync"])


@router.get("/ping", response_model=dict, tags=["Health"])
async def ping() -> dict:
    """
    Health check endpoint for readiness/liveness probes.
    """
    now: int = int(time.time())
    uptime: int = now - int(settings.service_start_time)
    return {
        "status": "ok",
        "uptime": uptime,
        "timestamp": now,
    }


@router.post(
    "/completion",
    tags=["completion", "llm", "sync", "model", "text"],
    description="Endpoint to generate text completions for a given input using a registered model.",
)
@cached(ttl=60)
async def completion(file: UploadFile = File(...)) -> dict:
    if file.content_type not in [
        ImageMimeTypes.JPEG,
        ImageMimeTypes.PNG,
    ]:
        raise HTTPException(status_code=400, detail="Image format not supported.")

    return {"data": "Placeholder for completion response"}
