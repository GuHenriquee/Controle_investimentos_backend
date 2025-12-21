import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Pega o caminho de onde este arquivo (config.py) está
# Ex: .../backend/app/core/config.py
CURRENT_FILE_DIR = Path(__file__).parent 

# 2. Sobe dois níveis para chegar na raiz do projeto
# .../backend/app/core/ -> .../backend/app/ -> .../backend/
PROJECT_ROOT = CURRENT_FILE_DIR.parent.parent

# 3. Aponta para o arquivo .env na raiz
ENV_PATH = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    # Suas variáveis (Verifique se os nomes batem com o .env)
    DATABASE_URL: str
    FRONT_URL: str
    SECRET_KEY: str
    FINNHUB_API_KEY: str
    COINCAP_API_KEY: str
    
    # OBS: No erro apareceu GITHUB_TOKE (sem N). 
    # Verifique se você escreveu errado aqui ou no .env. 
    # Vou assumir que o certo é GITHUB_TOKEN.
    GITHUB_TOKEN: str 

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,  # <--- Aqui usamos o caminho absoluto
        env_file_encoding='utf-8',
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()