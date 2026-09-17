import requests
from agent.agent import LostFoundAgent

base = "http://127.0.0.1:8001"

print("--- 1. Health Check ---")
r_health = requests.get(f"{base}/health")
assert r_health.status_code == 200, f"Health check failed: {r_health.text}"
print("Health Status:", r_health.json())

print("\n--- 2. Submitting Lost Item ---")
lost_payload = {
    "item_name": "Black Backpack",
    "description": "Black backpack with laptop compartment",
    "location": "Near Library",
    "lost_time": "2026-08-20T14:00:00",
    "contact": "+919876543210",
}
r_lost = requests.post(f"{base}/api/lost-items", json=lost_payload)
assert r_lost.status_code == 201, f"Failed to create lost item: {r_lost.text}"
lost_item = r_lost.json()
lost_id = lost_item["id"]
print(f"Created Lost Item #{lost_id}: {lost_item['item_name']} at {lost_item['location']}")

print("\n--- 3. Submitting YOLO Detection ---")
det_payload = {
    "camera_id": "CAM_03",
    "location": "Library Entrance",
    "object": "backpack",
    "confidence": 0.94,
    "timestamp": "2026-08-20T15:30:00",
    "image_path": "/results/detections/id1_jpg.rf.ea6996ec100286fada2274ef7e2a5c45.jpg",
}
r_det = requests.post(f"{base}/api/detections", json=det_payload)
assert r_det.status_code == 201, f"Failed to create detection: {r_det.text}"
detection = r_det.json()
det_id = detection["id"]
print(f"Created Detection #{det_id}: {detection['object']} at {detection['location']} (Confidence: {detection['confidence']})")

print("\n--- 4. Running Investigation Agent ---")
agent = LostFoundAgent()
result = agent.investigate(lost_id)
print("Agent Investigation Result:")
print("  Status:", result.get("status"))
print("  Match Score:", result.get("match_score"))
print("  Reason:", result.get("reason"))
print("  Match ID:", (result.get("match") or {}).get("id"))
print("  Alert ID:", (result.get("alert") or {}).get("id"))

print("\n--- 5. Verifying Match in Backend API ---")
match_record = result.get("match")
assert match_record is not None, "Expected match record to be created"
match_id = match_record["id"]
r_match = requests.get(f"{base}/api/matches/{match_id}")
assert r_match.status_code == 200, f"Failed to retrieve match: {r_match.text}"
print(f"Verified Match #{match_id} in backend: Decision = {r_match.json()['decision']}, Score = {r_match.json()['match_score']}")

print("\n--- 6. Verifying Alert in Backend API ---")
alert_record = result.get("alert")
if result.get("status") in ("MATCH", "MATCH_FOUND"):
    assert alert_record is not None, "Expected alert record for strong match"
    alert_id = alert_record["id"]
    r_alert = requests.get(f"{base}/api/alerts/{alert_id}")
    assert r_alert.status_code == 200, f"Failed to retrieve alert: {r_alert.text}"
    print(f"Verified Alert #{alert_id} in backend: Type = {r_alert.json()['alert_type']}, Message = '{r_alert.json()['message']}'")
else:
    print(f"Match status is {result.get('status')}; alert created: {alert_record is not None}")

print("\n--- 7. Verifying Investigation Memory ---")
memory = agent.get_memory()
print("Investigation Memory State:")
print("  Lost Item ID:", memory["lost_item_id"])
print("  Checked Detection IDs:", memory["checked_detections"])
print("  Searched Locations:", memory["searched_locations"])
print("  Best Match ID:", memory["best_match"])
print("  Best Score:", memory["best_score"])
print("  Investigation Status:", memory["status"])

print("\n--- 8. Verifying Frontend Service Data ---")
r_all_lost = requests.get(f"{base}/api/lost-items")
r_all_det = requests.get(f"{base}/api/detections")
r_all_matches = requests.get(f"{base}/api/matches")
r_all_alerts = requests.get(f"{base}/api/alerts")
print(f"Frontend Data Sources: {len(r_all_lost.json())} lost items, {len(r_all_det.json())} detections, {len(r_all_matches.json())} matches, {len(r_all_alerts.json())} alerts.")

print("\n=======================================================")
print(" ALL END-TO-END INTEGRATION TESTS PASSED SUCCESSFULLY! ")
print("=======================================================")
