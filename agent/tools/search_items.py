import requests

from agent.config import BACKEND_API_URL


def search_items():
    """Search open lost-item reports from the backend."""

    response = requests.get(
        f"{BACKEND_API_URL}/api/lost-items",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()