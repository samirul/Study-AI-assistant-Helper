"""Nodes used by the LangGraph workflow."""

from app.core.llm.models import get_chat_model
from app.core.llm.pydantic import IntentClassifier
from app.core.llm.prompts import INTENT_CLASSIFIER_SYSTEM_PROMPT
from app.core.llm.state import State


def classify_intent(state: State) -> dict[str, str]:
    """Classify the intent of the latest user message."""
    structured_llm = get_chat_model().with_structured_output(IntentClassifier)
    result = structured_llm.invoke([
        {
            "role": "system",
            "content": INTENT_CLASSIFIER_SYSTEM_PROMPT,
        },
        {"role": "user", "content": state["messages"][-1].content},
    ])

    return {"message_intent": result.message_intent}
