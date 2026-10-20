"""Adding all environment variables"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


def settings_config_func() -> SettingsConfigDict:
    """Return the shared settings configuration for environment variables."""
    return SettingsConfigDict(
        env_file=".env",
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
