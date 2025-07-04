# app/__init__.py
# This file can be left empty, or you can expose important objects for easier access.

from fastapi import FastAPI

__all__ = ["get_app", "CompletionModel"]


def get_app() -> FastAPI:
    """Return the FastAPI application lazily."""
    from app.main import app

    return app


try:  # Optional: allow tests to run without heavy deps
    from app.core.completion import CompletionModel
except Exception:  # pragma: no cover - safe fallback
    CompletionModel = None  # type: ignore
