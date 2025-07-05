import json
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import JSONResponse

from app.core.scan import process_scan

records_router = APIRouter(tags=["sync"])


@records_router.post("/scan", response_model=dict, tags=["Records"])
async def scan_record(request: Request) -> JSONResponse:
    """
    Scans an image, extracts text, and updates patient records.
    """
    image_base64 = (await request.body()).decode()
    result = await process_scan(image_base64)
    return JSONResponse(content=result)


@records_router.get("/records", response_model=dict, tags=["Records"])
async def get_records() -> JSONResponse:
    """
    Retrieve patient records.
    """
    try:
        with open("app/assets/patient.json", "r") as f:
            patient_data = json.load(f)
        return JSONResponse(content=patient_data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Patient records not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding patient records.")
