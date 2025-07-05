import logging
from app.core.api_request import api_request
from app.models.gemma import Content, GemmaPayload, Part

async def format_chat_response(text: str) -> str:
    """
    Formats the given text as a chat response using an LLM.
    """
    logging.info("Formatting chat response.")
    
    prompt = f"""You are a helpful assistant. Your task is to format the following text as a natural and friendly chat response.
    The response should be easy to read and understand.
    
    Original text:
    ---
    {text}
    ---
    
    Formatted response:
    """
    
    payload = GemmaPayload(contents=[Content(role="user", parts=[Part(text=prompt, inlineData=None)])])
    
    api_response = await api_request(payload)
    
    if api_response and api_response.get("data"):
        return api_response["data"]
    else:
        logging.error("Failed to format chat response from LLM.")
        return text
