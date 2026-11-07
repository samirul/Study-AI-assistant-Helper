"""Build and compile the application LangGraph workflow."""

from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from study_ai_assistant_helper.app.core.llm.nodes import (
    classify_intent,
    prompt_llm_chat,
    prompt_llm_rag,
    prompt_llm_summarize,
    summarize_previous_texts_or_data,
)
from study_ai_assistant_helper.app.core.llm.state import State
from study_ai_assistant_helper.app.graph.edges import configure_edges

NODE_REGISTRY = {
    "classifier": classify_intent,
    "chat_agent": prompt_llm_chat,
    "rag_agent": prompt_llm_rag,
    "summarize_agent": prompt_llm_summarize,
    "summarize_previous_texts_or_data": summarize_previous_texts_or_data,
}

NODE_NAMES = {
    node_name: node_name for node_name in NODE_REGISTRY
}


def create_graph() -> StateGraph:
    """Build and compile the application graph."""
    builder = StateGraph(State)

    for node_name, node in NODE_REGISTRY.items():
        builder.add_node(node_name, node)

    configure_edges(builder, NODE_NAMES)
    return builder.compile(checkpointer=InMemorySaver())