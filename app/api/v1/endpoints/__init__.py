from .chat import router as chat_router
from .clinical_trial_router import router as clinical_trial_router
from .records import records_router
from .websearch import router as websearch_router
from .webscraper import router as webscraper_router
from .gemma_web_search import router as gemma_web_search_router

__all__ = ["chat_router", "clinical_trial_router", "records_router", "websearch_router", "webscraper_router", "gemma_web_search_router"]
