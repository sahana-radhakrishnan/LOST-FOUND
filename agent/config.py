import os

from dotenv import load_dotenv

load_dotenv()

BACKEND_API_URL = os.getenv(
    "BACKEND_API_URL",
    "http://127.0.0.1:8001",
).rstrip("/")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
).rstrip("/")

QWEN_MODEL = os.getenv(
    "QWEN_MODEL",
    "qwen3:latest",
)

MATCH_THRESHOLD = float(
    os.getenv("MATCH_THRESHOLD", "0.60")
)

STRONG_MATCH_THRESHOLD = float(
    os.getenv("STRONG_MATCH_THRESHOLD", "0.85")
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")