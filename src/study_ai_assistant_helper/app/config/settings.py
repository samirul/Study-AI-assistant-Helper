"""Adding all environment variables"""

import os
from dotenv import load_dotenv
from pydantic import Field, SecretStr
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


class DatabaseSettings(BaseSettings):
    """PostgreSQL connection and async connection-pool settings."""

    model_config = settings_config_func()

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = Field(default=5432, gt=0, le=65535)
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    DB_POOL_SIZE: int = Field(default=5, gt=0)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0)
    DB_POOL_TIMEOUT_SECONDS: float = Field(default=30.0, gt=0)
    DB_POOL_RECYCLE_SECONDS: int = Field(default=1800, gt=0)


database_settings = DatabaseSettings()  # pyright: ignore[reportCallIssue]
