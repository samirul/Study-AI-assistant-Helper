"""Nodes used by the LangGraph workflow."""

from study_ai_assistant_helper.app.core.llm.models import get_chat_model
from study_ai_assistant_helper.app.core.llm.pydantic import IntentClassifier
from study_ai_assistant_helper.app.core.llm.prompts import (
    CHAT_SYSTEM_PROMPT,
    INTENT_CLASSIFIER_SYSTEM_PROMPT,
    RAG_SYSTEM_PROMPT,
    SUMMARIZE_SYSTEM_PROMPT,
    SUMMARIZE_REQUEST_REWRITE_PROMPT,
)
from study_ai_assistant_helper.app.core.llm.state import State
from study_ai_assistant_helper.app.core.llm.vectorstore import get_vector_store


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
    documents = get_vector_store().similarity_search(query=query, k=3)
    context = "\n".join(f"- {document.page_content}" for document in documents)
    messages = [
        {
            "role": "system",
            "content": RAG_SYSTEM_PROMPT.format(context=context),
        },
    ] + state["messages"]
    response = get_chat_model().invoke(messages)
    return {"messages": [{"role": "assistant", "content": response.content}]}

def prompt_llm_summarize(state: State) -> dict[str, list]:
    """Summarize relevant documents retrieved for the user's query."""
    query = state["messages"][-1].content
    documents = get_vector_store().similarity_search(query=query, k=3)
    context = "\n".join(f"- {document.page_content}" for document in documents)
    messages = [
        {
            "role": "system",
            "content": SUMMARIZE_SYSTEM_PROMPT.format(context=context),
        },
    ] + state["messages"]
    response = get_chat_model().invoke(messages)
    return {"messages": [{"role": "assistant", "content": response.content}]}


def summarize_previous_texts_or_data(state: State) -> dict[str, list]:
    """Rewrite the latest request as a clear instruction to summarize prior content."""
    messages = [
        {"role": "system", "content": SUMMARIZE_REQUEST_REWRITE_PROMPT},
    ] + state["messages"]

    response = get_chat_model().invoke(messages)
    return {"messages": [{"role": "user", "content": response.content}]}