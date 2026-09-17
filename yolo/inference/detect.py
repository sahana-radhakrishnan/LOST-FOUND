from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import cv2
import requests
from ultralytics import YOLO


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "models" / "best.pt"
DEFAULT_OUTPUT = ROOT / "results" / "detections"


def detect_images(
	source: str,
	model_path: str | Path = DEFAULT_MODEL,
	output_dir: str | Path = DEFAULT_OUTPUT,
	backend_url: str = "http://127.0.0.1:8001",
	camera_id: str = "CAM_01",
	location: str = "Unknown",
	confidence: float = 0.25,
) -> list[dict]:
	"""Run YOLO, save annotated images, and register detections in the API."""

	output_path = Path(output_dir)
	output_path.mkdir(parents=True, exist_ok=True)
	backend_url = backend_url.rstrip("/")
	model = YOLO(str(model_path))
	detections = []

	for result in model.predict(source=source, conf=confidence, stream=True):
		source_path = Path(str(result.path))
		annotated_name = f"{source_path.stem}_detected{source_path.suffix or '.jpg'}"
		annotated_path = output_path / annotated_name
		# Keep the stored image clean; the frontend highlights only the selected detection.
		cv2.imwrite(str(annotated_path), result.orig_img)

		names = result.names
		boxes = result.boxes
		timestamp = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()

		if boxes is None:
			continue

		for class_id, score, coordinates in zip(
			boxes.cls.tolist(), boxes.conf.tolist(), boxes.xyxy.tolist()
		):
			object_name = names[int(class_id)]
			payload = {
				"camera_id": camera_id,
				"location": location,
				"object": object_name,
				"confidence": float(score),
				"timestamp": timestamp,
				"image_path": f"/results/detections/{annotated_name}",
				"bbox": {
					"x1": float(coordinates[0]),
					"y1": float(coordinates[1]),
					"x2": float(coordinates[2]),
					"y2": float(coordinates[3]),
				},
			}
			response = requests.post(
				f"{backend_url}/api/detections",
				json=payload,
				timeout=10,
			)
			response.raise_for_status()
			detections.append(response.json())

	return detections


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run LOST-FOUND YOLO inference.")
	parser.add_argument("source", help="Image, directory, video, or camera source")
	parser.add_argument("--model", default=str(DEFAULT_MODEL))
	parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
	parser.add_argument("--backend-url", default="http://127.0.0.1:8001")
	parser.add_argument("--camera-id", default="CAM_01")
	parser.add_argument("--location", default="Unknown")
	parser.add_argument("--confidence", type=float, default=0.25)
	args = parser.parse_args()

	created = detect_images(
		source=args.source,
		model_path=args.model,
		output_dir=args.output,
		backend_url=args.backend_url,
		camera_id=args.camera_id,
		location=args.location,
		confidence=args.confidence,
	)
	print(f"Registered {len(created)} detections.")
