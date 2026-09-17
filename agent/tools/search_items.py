import requests

from agent.config import BACKEND_API_URL


def search_items(
    status: str = "LOST",
) -> list[dict]:
    """
    Search lost-item reports through the backend API.

    The agent never accesses the database directly.
    """

    response = requests.get(
        f"{BACKEND_API_URL}/api/lost-items",
        timeout=10,
    )

    response.raise_for_status()

    items = response.json()

    if status:
        items = [
            item
            for item in items
            if item.get("status") == status
        ]

    return items