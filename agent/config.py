import os

from dotenv import load_dotenv

load_dotenv()

BACKEND_API_URL = os.getenv(
    "BACKEND_API_URL",
    "http://localhost:8000",
).rstrip("/")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
).rstrip("/")

QWEN_MODEL = os.getenv(
    "QWEN_MODEL",
    "qwen3",
)

MATCH_THRESHOLD = 0.85
POSSIBLE_MATCH_THRESHOLD = 0.60