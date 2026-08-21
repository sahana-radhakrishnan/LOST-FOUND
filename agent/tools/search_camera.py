from datetime import datetime

from agent.tools.search_found_items import search_found_items


def search_camera(
    camera_id: str | None = None,
    location: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
) -> list[dict]:
    """
    Search detections by camera, location and/or time range.
    """

    detections = search_found_items()

    results = []

    start = (
        datetime.fromisoformat(start_time)
        if start_time
        else None
    )

    end = (
        datetime.fromisoformat(end_time)
        if end_time
        else None
    )

    for detection in detections:

        if (
            camera_id
            and detection.get("camera_id") != camera_id
        ):
            continue

        if (
            location
            and location.lower()
            not in detection.get(
                "location",
                "",
            ).lower()
        ):
            continue

        timestamp = detection.get("timestamp")

        if timestamp:
            detected_time = datetime.fromisoformat(
                timestamp
            )

            if start and detected_time < start:
                continue

            if end and detected_time > end:
                continue

        results.append(detection)

    return results