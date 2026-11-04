"""All LLM prompts"""

INTENT_CLASSIFIER_PROMPT_DESCRIPTION = {
    "prompt": "Look for weather the user wants to chat, ask for knowledge or summarize the text"
}

INTENT_CLASSIFIER_SYSTEM_PROMPT = (
    "Classify the latest user message as exactly one of: "
    "chat, knowledge, or summarization."
)
