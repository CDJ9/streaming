# app/config/settings.py

"""
Configuration settings for the app using Pydantic Settings.

- This version uses pydantic-settings to manage configuration.
"""

from pydantic_settings import BaseSettings  # Corrected import

class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://jitsi_user:yourpassword@localhost/str3aming"
    secret_key: str = "super-secret-key"
    jitsi_domain: str = "https://meet.jit.si"

    class Config:
        env_file = ".env"  # Load environment variables from .env file

settings = Settings()
