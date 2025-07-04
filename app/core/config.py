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

    model_config = SettingsConfigDict(env_file=".env")


# Initialize the settings object globally
settings = Settings()
