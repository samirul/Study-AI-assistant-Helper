"""LLM model related pydantic models"""

from typing import Literal
from pydantic import BaseModel, Field
from app.core.llm.prompts import INTENT_CLASSIFIER_PROMPT_DESCRIPTION

class IntentClassifier(BaseModel):
    """Classify whether a user message is chat, knowledge-seeking, or summarization."""
    message_intent: Literal['chat', 'knowledge', 'summarization'] = Field(
        ..., description= INTENT_CLASSIFIER_PROMPT_DESCRIPTION.get("prompt")
    )
