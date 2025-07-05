from __future__ import annotations

import time

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict


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
    google_cloud_project: str = Field(
        default="", alias="GOOGLE_CLOUD_PROJECT"
    )
    google_default_model: str = "gemini-1.5-flash-latest"
    static_files_dir: str = Field(default="static", alias="STATIC_FILES_DIR")

    model_config = SettingsConfigDict(env_file=".env")


# Initialize the settings object globally
settings = Settings()
