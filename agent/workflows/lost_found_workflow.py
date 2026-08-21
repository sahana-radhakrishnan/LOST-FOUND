from agent.tools.match_item import (
    create_match,
    match_item,
)

from agent.tools.search_found_items import (
    search_found_items,
)
from agent.tools.search_items import search_items
from agent.tools.send_sos import send_sos


class InvestigationMemory:
    """
    Maintains context for the current investigation session.
    """

    def __init__(self):
        self.context = {
            "lost_item_id": None,
            "item_name": None,
            "searched_locations": [],
            "checked_detections": [],
            "best_match": None,
            "best_score": 0.0,
            "status": None,
            "match_id": None,
        }

    def set_lost_item(self, lost_item: dict):
        self.context["lost_item_id"] = lost_item.get("id")
        self.context["item_name"] = lost_item.get(
            "item_name"
        )

    def add_location(self, location: str | None):
        if (
            location
            and location
            not in self.context["searched_locations"]
        ):
            self.context["searched_locations"].append(
                location
            )

    def add_detection(self, detection_id: int):
        if (
            detection_id
            not in self.context["checked_detections"]
        ):
            self.context["checked_detections"].append(
                detection_id
            )

    def has_checked_detection(
        self,
        detection_id: int,
    ) -> bool:
        return detection_id in self.context[
            "checked_detections"
        ]

    def update_best_match(
        self,
        detection_id: int,
        score: float,
    ):
        if score > self.context["best_score"]:
            self.context["best_match"] = detection_id
            self.context["best_score"] = score

    def set_status(self, status: str):
        self.context["status"] = status

    def set_match_id(self, match_id: int):
        self.context["match_id"] = match_id

    def get_context(self) -> dict:
        return self.context.copy()


class InvestigationWorkflow:
    """
    Coordinates the lost-and-found investigation.

    All backend communication is performed through tools.
    """

    def __init__(self):
        self.memory = InvestigationMemory()

    def find_lost_item(
        self,
        lost_item_id: int,
    ) -> dict | None:
        """
        Find a specific lost item from the backend.
        """

        items = search_items()

        for item in items:
            if item.get("id") == lost_item_id:
                return item

        return None

    def investigate(
        self,
        lost_item_id: int,
    ) -> dict:
        """
        Run the complete investigation.
        """

        # -----------------------------------
        # 1. Find lost item
        # -----------------------------------

        lost_item = self.find_lost_item(
            lost_item_id
        )

        if not lost_item:
            self.memory.set_status(
                "LOST_ITEM_NOT_FOUND"
            )

            return {
                "status": "LOST_ITEM_NOT_FOUND",
                "message": (
                    f"Lost item {lost_item_id} "
                    "was not found."
                ),
                "memory": self.memory.get_context(),
            }

        self.memory.set_lost_item(lost_item)

        self.memory.add_location(
            lost_item.get("location")
        )

        # -----------------------------------
        # 2. Search detections
        # -----------------------------------

        detections = search_found_items()

        candidates = []

        # -----------------------------------
        # 3. Compare detections
        # -----------------------------------

        for detection in detections:

            detection_id = detection.get("id")

            if detection_id is None:
                continue

            # Don't investigate the same detection twice.
            if self.memory.has_checked_detection(
                detection_id
            ):
                continue

            self.memory.add_detection(
                detection_id
            )

            self.memory.add_location(
                detection.get("location")
            )

            # --------------------------------
            # 4. Calculate match
            # --------------------------------

            result = match_item(
                lost_item,
                detection,
                description_score=self.calculate_description_score(
                    lost_item,
                    detection,
                ),
            )

            score = result["match_score"]

            self.memory.update_best_match(
                detection_id,
                score,
            )

            candidates.append(
                {
                    "detection": detection,
                    "result": result,
                }
            )

        # -----------------------------------
        # 5. No detections
        # -----------------------------------

        if not candidates:
            self.memory.set_status("NO_MATCH")

            return {
                "status": "NO_MATCH",
                "message": (
                    "No new detections were "
                    "available for investigation."
                ),
                "memory": self.memory.get_context(),
            }

        # -----------------------------------
        # 6. Find best candidate
        # -----------------------------------

        best_candidate = max(
            candidates,
            key=lambda candidate: candidate[
                "result"
            ]["match_score"],
        )

        detection = best_candidate["detection"]
        result = best_candidate["result"]

        score = result["match_score"]
        decision = result["decision"]
        reason = result["reason"]

        # -----------------------------------
        # 7. NO_MATCH
        # -----------------------------------

        if decision == "NO_MATCH":
            self.memory.set_status("NO_MATCH")

            return {
                "status": "NO_MATCH",
                "lost_item": lost_item,
                "best_detection": detection,
                "match_score": score,
                "decision": decision,
                "reason": reason,
                "memory": self.memory.get_context(),
            }

        # -----------------------------------
        # 8. Create backend match
        # -----------------------------------

        match = create_match(
            lost_item_id=lost_item["id"],
            detection_id=detection["id"],
            match_score=score,
            decision=decision,
            reason=reason,
        )

        self.memory.set_match_id(
            match.get("id")
        )

        self.memory.set_status(decision)

        # -----------------------------------
        # 9. Strong match → alert
        # -----------------------------------

        alert = None

        if decision == "MATCH":

            message = (
                f"{lost_item.get('item_name')} "
                f"possibly found near "
                f"{detection.get('location', 'unknown location')}"
            )

            alert = send_sos(
                match_id=match["id"],
                alert_type="POSSIBLE_MATCH",
                message=message,
                status="PENDING",
            )

        return {
            "status": decision,
            "lost_item": lost_item,
            "best_detection": detection,
            "match": match,
            "alert": alert,
            "match_score": score,
            "reason": reason,
            "memory": self.memory.get_context(),
        }

    @staticmethod
    def calculate_description_score(
        lost_item: dict,
        detection: dict,
    ) -> float:
        """
        Temporary deterministic description score.

        The detection API currently has no description field.
        Therefore we compare the lost-item description against
        the detected object's name.

        This can later be replaced with nomic-embed-text
        semantic similarity without changing the API contract.
        """

        description = (
            lost_item.get("description", "")
            .lower()
        )

        detected_object = (
            detection.get("object", "")
            .lower()
        )

        if not description or not detected_object:
            return 0.0

        description_words = set(
            description.split()
        )

        object_words = set(
            detected_object.split()
        )

        if detected_object in description:
            return 1.0

        overlap = description_words & object_words

        if not overlap:
            return 0.0

        return min(
            len(overlap) / len(object_words),
            1.0,
        )