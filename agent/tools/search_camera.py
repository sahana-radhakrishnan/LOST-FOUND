from datetime import datetime
from typing import Optional

from agent.config import BACKEND_API_URL
import requests


def search_camera(
    camera_id: Optional[str] = None,
    location: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
):
    """
    Search detections using camera, location, and time filters.
    """

    response = requests.get(
        f"{BACKEND_API_URL}/api/detections",
        timeout=10,
    )

    response.raise_for_status()

    detections = response.json()

    if not isinstance(detections, list):
        return []

    results = []

    for detection in detections:

        if camera_id:
            if detection.get("camera_id") != camera_id:
                continue

        if location:
            detection_location = str(
                detection.get("location", "")
            ).lower()

            if location.lower() not in detection_location:
                continue

        detected_at = detection.get("detected_at")

        if detected_at and start_time:
            if detected_at < start_time:
                continue

        if detected_at and end_time:
            if detected_at > end_time:
                continue

        results.append(detection)

    return results