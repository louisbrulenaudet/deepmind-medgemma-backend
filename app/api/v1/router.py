from fastapi import APIRouter

from app.api.v1.endpoints import sync_router

router = APIRouter()

# Include all routers
router.include_router(sync_router)
