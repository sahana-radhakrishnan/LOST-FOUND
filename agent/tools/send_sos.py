import requests

from agent.config import BACKEND_API_URL


def send_sos(
    match_id: int,
    alert_type: str,
    message: str,
    status: str = "PENDING",
) -> dict:
    """
    Create an investigation alert through the backend.
    """

    payload = {
        "match_id": match_id,
        "alert_type": alert_type,
        "message": message,
        "status": status,
    }

    response = requests.post(
        f"{BACKEND_API_URL}/api/alerts",
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()