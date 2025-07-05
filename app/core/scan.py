import json
from fastapi import HTTPException
import binascii

from app.core.api_request import api_request
from app.models.gemma import GemmaPayload, Content, Part
from app.utils.image_processing import pad_base64_string


async def process_scan(image_base64: str) -> dict:
    try:
        mime_type = "image/jpeg"  # Default MIME type
        # Extract mime type and data from data URI
        if image_base64.startswith("data:image"):
            header, image_base64 = image_base64.split(",", 1)
            mime_type = header.split(":")[1].split(";")[0]

        # Clean base64 string by removing whitespace and newlines
        image_base64 = "".join(image_base64.split())

        # Pad the base64 string
        image_base64 = pad_base64_string(image_base64)

        # Prepare the payload for the Gemini API
        payload = GemmaPayload(
            contents=[
                Content(
                    role="user",
                    parts=[
                        Part(text="Extract the text from this image."),
                        Part(
                            inlineData={
                                "mimeType": mime_type,
                                "data": image_base64,
                            }
                        )
                    ]
                )
            ]
        )

        # Call the Gemini API
        response = await api_request(payload, model="gemini-1.5-flash")
        if response["status"] != "success":
            raise HTTPException(
                status_code=500, detail=f"Gemini API error: {response['error_message']}"
            )

        ocr_text = response["data"]

        # Update patient.json
        with open("app/assets/patient.json", "r+") as f:
            patient_data = json.load(f)
            # Assuming the OCR text should be added to a new field "ocr_results"
            if "ocr_results" not in patient_data:
                patient_data["ocr_results"] = []
            patient_data["ocr_results"].append(ocr_text)
            f.seek(0)
            json.dump(patient_data, f, indent=4)
            f.truncate()

        return {"status": "success", "ocr_text": ocr_text}

    except binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid base64 string.")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Patient records not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding patient records.")
