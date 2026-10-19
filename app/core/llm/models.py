"""Models configuration"""

from functools import lru_cache
from langchain_groq import ChatGroq
from langchain_ollama import OllamaEmbeddings
from app.config.settings import llm_model_settings

env_key = llm_model_settings

@lru_cache()
def get_chat_model() -> ChatGroq:
    """Return the configured Groq chat model."""
    return ChatGroq(
        model = env_key.CHAT_MODEL_GROQ,
        temperature=0.7,
        api_key=env_key.GROQ_API_KEY 
    )


@lru_cache()
def get_embedded_model() -> OllamaEmbeddings:
    """Return the configured Ollama embedding model."""
    return OllamaEmbeddings(
        model = env_key.RAG_EMBEDDING_MODEL,
        dimensions=1536
)