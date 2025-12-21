from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_FILE_DIR = Path(__file__).parent 

PROJECT_ROOT = CURRENT_FILE_DIR.parent.parent

ENV_PATH = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    FRONT_URL: str
    SECRET_KEY: str
    FINNHUB_API_KEY: str
    COINCAP_API_KEY: str
    GITHUB_TOKEN: str 

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, 
        env_file_encoding='utf-8',
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()