from datetime import datetime
from difflib import SequenceMatcher


def text_similarity(value1, value2):
    if not value1 or not value2:
        return 0.0

    value1 = str(value1).lower().strip()
    value2 = str(value2).lower().strip()

    return SequenceMatcher(
        None,
        value1,
        value2,
    ).ratio()


def time_similarity(lost_time, detected_time):
    if not lost_time or not detected_time:
        return 0.0

    try:
        lost = datetime.fromisoformat(
            lost_time.replace("Z", "+00:00")
        )

        detected = datetime.fromisoformat(
            detected_time.replace("Z", "+00:00")
        )

        difference_minutes = abs(
            (lost - detected).total_seconds()
        ) / 60

        if difference_minutes <= 15:
            return 1.0

        if difference_minutes <= 30:
            return 0.8

        if difference_minutes <= 60:
            return 0.6

        if difference_minutes <= 180:
            return 0.3

        return 0.0

    except (ValueError, TypeError):
        return 0.0


def match_item(lost_item, detection):
    """
    Calculate weighted match score.

    Object:       40%
    Description:  20%
    Location:     20%
    Time:         10%
    Confidence:   10%
    """

    object_score = text_similarity(
        lost_item.get("item_name"),
        detection.get("object_name"),
    )

    description_score = text_similarity(
        lost_item.get("description"),
        detection.get("description", ""),
    )

    location_score = text_similarity(
        lost_item.get("location"),
        detection.get("location"),
    )

    time_score = time_similarity(
        lost_item.get("lost_time"),
        detection.get("detected_at"),
    )

    confidence = float(
        detection.get("confidence", 0.0)
    )

    confidence = max(0.0, min(confidence, 1.0))

    final_score = (
        object_score * 0.40
        + description_score * 0.20
        + location_score * 0.20
        + time_score * 0.10
        + confidence * 0.10
    )

    if final_score >= 0.85:
        decision = "MATCH_FOUND"
    elif final_score >= 0.60:
        decision = "POSSIBLE_MATCH"
    else:
        decision = "NO_MATCH"

    reason = (
        f"Object={object_score:.2f}, "
        f"Description={description_score:.2f}, "
        f"Location={location_score:.2f}, "
        f"Time={time_score:.2f}, "
        f"Confidence={confidence:.2f}"
    )

    return {
        "match_score": round(final_score, 4),
        "decision": decision,
        "reason": reason,
    }