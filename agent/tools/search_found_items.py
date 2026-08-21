import requests

from agent.config import BACKEND_API_URL


def search_found_items() -> list[dict]:
    """
    Search YOLO-generated detections through the backend API.
    """

    response = requests.get(
        f"{BACKEND_API_URL}/api/detections",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()