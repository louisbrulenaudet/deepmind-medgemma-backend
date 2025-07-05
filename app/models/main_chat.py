from pydantic import BaseModel


class ChatInput(BaseModel):
    conversation: list[dict[str, str]]


class MultimodalInput(BaseModel):
    medical_file: str
    text_input: str = ""
    uploaded_files: list[dict[str, str]] = []
