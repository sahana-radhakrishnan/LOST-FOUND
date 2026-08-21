from langchain_ollama import ChatOllama

from agent.config import OLLAMA_BASE_URL, QWEN_MODEL


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=QWEN_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )