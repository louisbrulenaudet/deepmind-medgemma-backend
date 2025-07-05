import json
from fastapi import HTTPException
import binascii
from pydantic import ValidationError

from app.core.api_request import api_request
from app.models.gemma import GemmaPayload
from app.models.scan import PatientRecord
from app.utils.image_processing import pad_base64_string
from app.utils.json_utils import deep_merge


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
        Analyze the attached image and extract any new or updated information for the patient.
        The current patient data is:
        {json.dumps(patient_data, indent=4)}

        Return ONLY a JSON object containing the new or updated fields, without any additional text, comments, or markdown formatting.
        For example, if you find a new lab result, return:
        {{
            "lab_results": [
                {{
                    "date": "YYYY-MM-DD",
                    "sodium_mmol_per_L": 140,
                    "potassium_mmol_per_L": 4.1,
                    "creatinine_umol_per_L": 90
                }}
            ]
        }}
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
        
        # Clean the response to ensure it's valid JSON
        if updated_patient_data_str.startswith("```json"):
            updated_patient_data_str = updated_patient_data_str[7:]
        if updated_patient_data_str.endswith("```"):
            updated_patient_data_str = updated_patient_data_str[:-3]
        
        updated_patient_data_str = updated_patient_data_str.strip()
        
        try:
            new_data = json.loads(updated_patient_data_str)
            merged_data = deep_merge(patient_data, new_data)
            patient_record = PatientRecord.parse_obj(merged_data)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to decode JSON from model response: {updated_patient_data_str}",
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Invalid data structure after merging: {e}",
            )

        with open("app/assets/patient.json", "w") as f:
            json.dump(patient_record.dict(), f, indent=4)

        return patient_record.dict()

    except binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid base64 string.")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Patient records not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding patient records.")
