import requests
from agent.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(message: str) -> dict:
    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendMessage"
    )
    response = requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()