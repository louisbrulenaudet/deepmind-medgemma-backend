from .chat import router as sync_router
from .clinical_trial_router import router as clinical_trial_router
from .websearch import router as websearch_router

__all__ = ["sync_router", "clinical_trial_router", "websearch_router"]
