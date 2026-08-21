from typing import Any


class InvestigationMemory:
    def __init__(self):
        self.context = {
            "lost_item_id": None,
            "item_name": None,
            "searched_locations": [],
            "checked_detections": [],
            "best_match": None,
            "best_score": 0.0,
            "status": None,
        }

    def set_lost_item(self, lost_item):
        self.context["lost_item_id"] = lost_item.get(
            "lost_item_id",
            lost_item.get("id"),
        )

        self.context["item_name"] = lost_item.get(
            "item_name"
        )

    def add_location(self, location):
        if (
            location
            and location not in self.context["searched_locations"]
        ):
            self.context["searched_locations"].append(location)

    def add_detection(self, detection_id):
        if (
            detection_id
            and detection_id
            not in self.context["checked_detections"]
        ):
            self.context["checked_detections"].append(
                detection_id
            )

    def update_best_match(self, detection_id, score):
        if score > self.context["best_score"]:
            self.context["best_match"] = detection_id
            self.context["best_score"] = score

    def set_status(self, status):
        self.context["status"] = status

    def get_context(self):
        return self.context.copy()