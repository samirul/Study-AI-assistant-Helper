"""Adding all environment variables"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

def is_production() -> bool:
    """Return whether the deployment mode is production."""
    mode = os.getenv("DEPLOYMENT_MODE", "development").strip().lower()
    if mode not in {"development", "dev", "production", "prod"}:
        raise ValueError(f"Invalid DEPLOYMENT_MODE: {mode!r}")
    return mode in {"production", "prod"}

def settings_config_func() -> SettingsConfigDict:
    """Return the shared settings configuration for environment variables."""
    return SettingsConfigDict(
        env_file=".env.prod" if is_production() else ".env.dev",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class LLMModelSettings(BaseSettings):
    """Model settings loaded from environment variables."""

    model_config = settings_config_func()

    GROQ_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    PINECONE_API_KEY: str | None = None
    CHAT_MODEL_GROQ: str | None = None
    RAG_EMBEDDING_MODEL: str | None = None
    RAG_EMBEDDING_MODEL_DIMENSIONAL_VALUE: str | None = None


llm_model_settings = LLMModelSettings()


class PineConeSettings(BaseSettings):
    """Pinecone settings loaded from environment variables."""

    model_config = settings_config_func()

    PINECONE_API_KEY: str | None = None
    PINECONE_INDEX_NAME: str | None = None
    PINECONE_DIMENSIONAL_VALUE: str | None = None


pine_cone_settings = PineConeSettings()

class RecursiveCharacterTextSplitterSettings(BaseSettings):
    """Text splitter settings loaded from environment variables."""

    model_config = settings_config_func()
    
    RECURSIVE_SPLITTER_CHUNK_SIZE: str | None = None
    RECURSIVE_SPLITTER_CHUNK_OVERLAP: str | None = None

recursive_splitter_settings = RecursiveCharacterTextSplitterSettings()

class FastAPIBaseSettings(BaseSettings):
    """FastAPI settings loaded from environment variables."""

    model_config = settings_config_func()

    FAST_API_SECRET_KEY: str

fast_api_base_settings = FastAPIBaseSettings()
