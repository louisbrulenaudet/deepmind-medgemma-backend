from typing import Any

import httpx

from app.core.config import settings

__all__ = [
    "api_request",
]


async def api_request(
    payload: object, model: str | None = None, method: str | None = None
) -> dict[str, Any]:
    response = {
        "status": "success",
        "error_message": "",
        "model": model,
        "data": None,
    }

    if not payload:
        response["status"] = "error"
        response["error_message"] = "Invalid payload argument"
        return response

    if model is None:
        model = settings.google_default_model
        response["model"] = model

    if method is None:
        method = settings.google_api_default_method

    url = f"{settings.google_api_base_url}{model}:{method}?key={settings.api_key}"

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, json=payload)
            res.raise_for_status()
            data = res.json()

            if (
                "candidates" not in data
                or "content" not in data["candidates"][0]
                or "parts" not in data["candidates"][0]["content"]
                or "text" not in data["candidates"][0]["content"]["parts"][0]
            ):
                response["status"] = "error"
                response["error_message"] = "Error or no text returned"
                return response

            response["full_data"] = data
            response["data"] = data["candidates"][0]["content"]["parts"][0]["text"]

        except httpx.RequestError as e:
            response["status"] = "error"
            response["error_message"] = str(e)

    return response
