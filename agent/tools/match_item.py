from datetime import datetime

import requests

from agent.config import (
    BACKEND_API_URL,
    STRONG_MATCH_THRESHOLD,
)

def text_similarity(first: str, second: str) -> float:
    """Calculate similarity between a lost-item name and YOLO object class."""

    first_tokens = set(first.lower().split())
    second_tokens = set(second.lower().split())

    if not first_tokens or not second_tokens:
        return 0.0

    # Exact match
    if first.lower().strip() == second.lower().strip():
        return 1.0

    # If the YOLO class is contained in the lost item name,
    # treat it as a strong category match.
    # Example: "Blue Backpack" -> "backpack"
    if second.lower().strip() in first.lower().strip():
        return 1.0

    # Normal token overlap for other cases
    intersection = first_tokens & second_tokens
    union = first_tokens | second_tokens

    return len(intersection) / len(union)


def location_similarity(
    lost_location: str,
    detection_location: str,
) -> float:
    """Compare lost and detection locations."""

    lost = lost_location.lower().strip()
    detection = detection_location.lower().strip()

    if not lost or not detection:
        return 0.0

    if lost == detection:
        return 1.0

    if lost in detection or detection in lost:
        return 0.8

    lost_tokens = set(lost.split())
    detection_tokens = set(detection.split())

    overlap = lost_tokens & detection_tokens

    if not overlap:
        return 0.0

    return len(overlap) / len(
        lost_tokens | detection_tokens
    )


def time_similarity(
    lost_time: str,
    detection_time: str,
) -> float:
    """Compare lost and detection timestamps."""

    try:
        lost = datetime.fromisoformat(lost_time)
        detected = datetime.fromisoformat(detection_time)

        difference_hours = abs(
            (lost - detected).total_seconds()
        ) / 3600

        if difference_hours <= 1:
            return 1.0

        if difference_hours <= 3:
            return 0.8

        if difference_hours <= 6:
            return 0.5

        if difference_hours <= 12:
            return 0.3

        return 0.0

    except (ValueError, TypeError):
        return 0.0


def match_item(
    lost_item: dict,
    detection: dict,
    description_score: float = 0.0,
) -> dict:
    """
    Compare a lost item with a detected object.

    Weighted score:

    Object similarity       40%
    Description similarity  20%
    Location similarity    20%
    Time similarity        10%
    Detection confidence   10%
    """

    object_score = text_similarity(
        lost_item.get("item_name", ""),
        detection.get("object", ""),
    )

    location_score = location_similarity(
        lost_item.get("location", ""),
        detection.get("location", ""),
    )

    time_score = time_similarity(
        lost_item.get("lost_time", ""),
        detection.get("timestamp", ""),
    )

    detection_confidence = float(
        detection.get("confidence", 0.0)
    )

    final_score = (
        object_score * 0.40
        + description_score * 0.20
        + location_score * 0.20
        + time_score * 0.10
        + detection_confidence * 0.10
    )

    final_score = round(
        min(max(final_score, 0.0), 1.0),
        4,
    )

    if final_score >= STRONG_MATCH_THRESHOLD:
        decision = "MATCH"
    elif final_score >= 0.60:
        decision = "POSSIBLE_MATCH"
    else:
        decision = "NO_MATCH"

    reason = (
        f"Object similarity: {object_score:.2f}; "
        f"description similarity: {description_score:.2f}; "
        f"location similarity: {location_score:.2f}; "
        f"time similarity: {time_score:.2f}; "
        f"detection confidence: {detection_confidence:.2f}"
    )

    return {
        "match_score": final_score,
        "decision": decision,
        "reason": reason,
    }

def create_match(
    lost_item_id: int,
    detection_id: int,
    match_score: float,
    decision: str,
    reason: str,
) -> dict:

    payload = {
        "lost_item_id": lost_item_id,
        "detection_id": detection_id,
        "match_score": match_score,
        "decision": decision,
        "reason": reason,
    }

    response = requests.post(
        f"{BACKEND_API_URL}/api/matches",
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()