import requests

from agent.config import BACKEND_API_URL


def send_sos(match_id, alert_type, message):
    """Create an alert through the backend."""

    payload = {
        "match_id": match_id,
        "alert_type": alert_type,
        "message": message,
        "status": "PENDING",
    }

    response = requests.post(
        f"{BACKEND_API_URL}/api/alerts",
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()