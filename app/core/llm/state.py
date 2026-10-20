"""Custom MessagesState from langgraph.graph"""

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    """Track the conversation messages, classified intent, and next graph node."""
    messages: Annotated[list, add_messages]
    message_intent: str | None
