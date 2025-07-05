import logging
from app.core.api_request import api_request
from app.models.gemma import GemmaPayload, Content, Part

async def classify_request(user_input: str) -> str:
    """
    Classifies the user's request into one of the following categories:
    - medgemma
    - clinical_trials
    - web_search
    """
    prompt = f"""
    Please classify the following user request into one of these categories: "medgemma", "clinical_trials", or "web_search". Depending on the user request, you may classify it as follows:
    - "medgemma": for requests about general information about medicine.
    - "clinical_trials": for requests about clinical trials. For example, "What clinical trials are available for diabetes?".
    - "web_search": for requests explicitly involving web searching. For example, "Search for hospital location specializing in diabetes treatment in Paris.".

    User request: "{user_input}"

    Classification:
    """

    payload = GemmaPayload(
        contents=[
            Content(
                role="user",
                parts=[
                    Part(text=prompt, inlineData=None)
                ]
            )
        ]
    )

    try:
        response = await api_request(payload)
        classification = response.get("data", "").strip().lower()
        
        if "medgemma" in classification:
            return "medgemma"
        elif "clinical_trials" in classification:
            return "clinical_trials"
        elif "web_search" in classification:
            return "web_search"
        else:
            logging.warning(f"Could not classify request, defaulting to medgemma. Response: {response}")
            return "medgemma"

    except Exception as e:
        logging.error(f"Error classifying request: {e}")
        return "medgemma"
