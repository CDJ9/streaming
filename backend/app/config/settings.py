# app/config/settings.py

"""
Configuration settings for the app using Pydantic Settings.

- This version is updated for local MiroTalk integration.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://jitsi_user:yourpassword@localhost/str3aming"
    secret_key: str = "super-secret-key"

    class Config:
        env_file = ".env"  # Load environment variables from .env file

settings = Settings()
