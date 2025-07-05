import json
from fastapi import HTTPException
import binascii

from app.core.api_request import api_request
from app.models.gemma import GemmaPayload
from app.utils.image_processing import pad_base64_string


async def process_scan(image_base64: str) -> dict:
    try:
        mime_type = "image/jpeg"  # Default MIME type
        if image_base64.startswith("data:image"):
            header, image_base64 = image_base64.split(",", 1)
            mime_type = header.split(":")[1].split(";")[0]

        image_base64 = "".join(image_base64.split())
        image_base64 = pad_base64_string(image_base64)

        with open("app/assets/patient.json", "r") as f:
            patient_data = json.load(f)

        prompt = f"""
        Analyze the attached image and update the patient's information based on any new details found.
        The current patient data is:
        {json.dumps(patient_data, indent=4)}

        Return ONLY the updated JSON object, without any additional text, comments, or markdown formatting.
        """

        payload_dict = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {"inlineData": {"mimeType": mime_type, "data": image_base64}},
                    ],
                }
            ]
        }
        payload = GemmaPayload.parse_obj(payload_dict)

        response = await api_request(payload, model="gemini-1.5-flash")
        if response["status"] != "success":
            raise HTTPException(
                status_code=500, detail=f"Gemini API error: {response['error_message']}"
            )

        updated_patient_data_str = response["data"].strip()        
        try:
            updated_patient_data = json.loads(updated_patient_data_str)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to decode JSON from model response: {updated_patient_data_str}",
            )

        with open("app/assets/patient.json", "w") as f:
            json.dump(updated_patient_data, f, indent=4)

        return updated_patient_data

    except binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid base64 string.")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Patient records not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding patient records.")
