import json
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

router = APIRouter(tags=["sync"])

@router.get("/records", response_model=dict, tags=["Records"])
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
