from fastapi import APIRouter

from app.api.v1.endpoints import (
    chat_router,
    clinical_trial_router,
    records_router,
    websearch_router,
)

router = APIRouter()

# Include all routers
router.include_router(chat_router)
router.include_router(records_router)
router.include_router(clinical_trial_router)
router.include_router(websearch_router)