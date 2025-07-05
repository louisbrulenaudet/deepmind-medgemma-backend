import time

from pydantic import Field
from pydantic.functional_validators import model_validator
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

import chromadb
from chromadb.config import Settings as ChromadbSettings
from chromadb.utils import embedding_functions


class Settings(BaseSettings):
    """
    Configuration settings for the application, using Pydantic for validation.
    """

    name: str = Field(default="JSON-ld", alias="APP_NAME")
    service_start_time: float = Field(default_factory=time.time, exclude=True)
    api_key: str = Field(default="", alias="API_KEY")
    google_api_base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta/models/",
        alias="GOOGLE_API_BASE_URL",
    )
    google_api_default_method: str = "generateContent"
    google_default_model: str = "gemini-1.5-flash-latest"
    static_files_dir: str = Field(default="static", alias="STATIC_FILES_DIR")
    chroma_client: None = None
    chroma_collection: None = None

    @model_validator(mode="after")
    def initialize_chroma_client(self) -> "Settings":
        self.chroma_client = chromadb.PersistentClient(
            path="chromadb", settings=ChromadbSettings(anonymized_telemetry=False)
        )

        print("ChromaDB client initialized successfully. Downloading embedding model...")  # noqa: T201

        sentence_transformer_ef = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="thomas-sounack/BioClinical-ModernBERT-base",
                device="mps",
                trust_remote_code=True,
            )
        )

        print("Embedding model downloaded successfully.")  # noqa: T201

        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name="clinical_trials", embedding_function=sentence_transformer_ef
        )

        return self

    model_config = SettingsConfigDict(env_file=".env")


# Initialize the settings object globally
settings = Settings()
