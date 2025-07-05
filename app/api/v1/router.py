from fastapi import APIRouter

from app.api.v1.endpoints import clinical_trial_router, sync_router, websearch_router

router = APIRouter()

# Include all routers
router.include_router(sync_router)
router.include_router(clinical_trial_router)
router.include_router(websearch_router)
