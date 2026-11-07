"""All LLM prompts"""

INTENT_CLASSIFIER_PROMPT_DESCRIPTION = {
    "prompt": "Look for weather the user wants to chat, ask for knowledge or summarize the text"
}

INTENT_CLASSIFIER_SYSTEM_PROMPT = (
    "Classify the latest user message as exactly one of: "
    "chat, knowledge, or summarization."
)

CHAT_SYSTEM_PROMPT = "You are a talkative and friendly chatbot. Be kind and helpful."

RAG_SYSTEM_PROMPT = (
    "You are a RAG assistant. Answer the user using only the context below. "
    "If the answer is not in the context, state that you do not have that "
    "information.\n\nContext:\n{context}"
)

SUMMARIZE_SYSTEM_PROMPT = (
    "Summarize the provided context clearly and accurately. Use only the "
    "context below; if the requested text is not present, state that you "
    "do not have that information.\n\nContext:\n{context}"
)

SUMMARIZE_REQUEST_REWRITE_PROMPT = (
    "Rewrite the latest user text-summarization request as a clear instruction "
    "for summarization, using the conversation history as context. Output only "
    "the rewritten instruction, without explanation."
)
