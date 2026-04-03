from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    app_name : str ="Communities AI Assistant"
    app_description : str = "Communities AI Assistant Description"
    debug: bool = False
    llm_api_key : str = "asdf"
    cascading_model : str =  "groq:qwen/qwen3-32b"
    models :List[str] = ["groq:openai/gpt-oss-120b", "groq:qwen/qwen3-32b","groq:whisper-large-v3-turbo"]
    token_expiry_time : int = 30
    jwt_secret_code : str = "VishalMali"
    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings()->Settings:
    return Settings()
