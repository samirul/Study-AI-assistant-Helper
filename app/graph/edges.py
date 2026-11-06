"""Configure intent routing and edges for the application graph."""

from langgraph.graph import END, START
from app.core.llm.state import State


INTENT_ROUTES = {
    "chat": "chat_agent",
    "knowledge": "rag_agent",
    "summarization": "summarize_previous_texts_or_data",
}

TERMINAL_NODES = (
    "chat_agent",
    "rag_agent",
    "summarize_agent",
)


def route_by_intent(state: State) -> str:
    """Resolve an intent to its destination node."""
    intent = state["message_intent"]

    try:
        INTENT_ROUTES[intent]
    except (KeyError, TypeError) as error:
        raise ValueError(f"Unsupported intent: {intent!r}") from error
    return intent


def configure_edges(
    builder,
    node_names: dict[str, str],
    terminal_nodes: tuple[str, ...] = TERMINAL_NODES,
) -> None:
    """Add the graph entry, intent routes, rewrite flow, and terminal edges."""
    builder.add_edge(START, node_names["classifier"])
    builder.add_edge(
        node_names["summarize_previous_texts_or_data"],
        node_names["summarize_agent"],
    )
    builder.add_conditional_edges(
        node_names["classifier"],
        route_by_intent,
        {
            intent: node_names[destination]
            for intent, destination in INTENT_ROUTES.items()
        },
    )
    for terminal_node in terminal_nodes:
        builder.add_edge(node_names[terminal_node], END)
