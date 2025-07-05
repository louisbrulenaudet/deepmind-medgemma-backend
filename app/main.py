from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from starlette.responses import JSONResponse
from dotenv import load_dotenv

from app._exceptions import CoreError
from app.api.v1.router import router as api_router
from app.core.config import settings

load_dotenv()

app = FastAPI(
    title=settings.name,
    description="Hackaton Google : Solve for Healthcare & Life Sciences with Gemma",
    version="0.1.0",
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(CoreError)
async def error_handler(_: Request, exc: CoreError) -> JSONResponse:
    """
    Custom exception handler for BusinessLogicError.
    Converts the error into a structured JSON response.
    """
    # Map specific exceptions to status codes
    status_codes = {
        "TaskNotFoundError": 404,
        "TaskInitalizationError": 500,
    }

    # Default to 400 if not specified
    status_code = status_codes.get(exc.__class__.__name__, 400)

    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "code": exc.code,
            "details": exc.details or {},
        },
    )
