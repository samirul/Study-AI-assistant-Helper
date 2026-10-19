"""Adding all environment variables"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class LLMModelSettings(BaseSettings):
    GROQ_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    PINECONE_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

llm_model_settings = LLMModelSettings()