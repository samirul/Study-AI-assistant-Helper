"""Nodes used by the LangGraph workflow."""

from app.core.llm.models import get_chat_model
from app.core.llm.pydantic import IntentClassifier
from app.core.llm.prompts import (
    CHAT_SYSTEM_PROMPT,
    INTENT_CLASSIFIER_SYSTEM_PROMPT,
    RAG_SYSTEM_PROMPT,
)
from app.core.llm.state import State
from app.core.llm.vectorstore import get_vector_store


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


def prompt_llm_chat(state: State) -> dict[str, list]:
    """Generate a chat response for the current conversation state."""
    messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}] + state["messages"]
    response = get_chat_model().invoke(messages)
    return {"messages": [{"role": "assistant", "content": response.content}]}


def prompt_llm_rag(state: State) -> dict[str, list]:
    """Generate a response to the latest user question using retrieved context."""
    query = state["messages"][-1].content
    documents = get_vector_store().similarity_search(query=query, k=7)
    context = "\n".join(f"- {document.page_content}" for document in documents)
    messages = [
        {
            "role": "system",
            "content": RAG_SYSTEM_PROMPT.format(context=context),
        },
    ] + state["messages"]
    response = get_chat_model().invoke(messages)
    return {"messages": [{"role": "assistant", "content": response.content}]}