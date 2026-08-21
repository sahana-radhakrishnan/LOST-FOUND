import requests

from agent.config import BACKEND_API_URL


def search_found_items():
    """Search detected/found items."""

    response = requests.get(
        f"{BACKEND_API_URL}/api/detections",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()