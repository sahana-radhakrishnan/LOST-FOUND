## Components

- `frontend`: React/Vite dashboard for reports, detections, matches, and alerts.
- `backend`: FastAPI REST API with SQLAlchemy models and MySQL persistence.
- `agent`: Python investigation workflow. It communicates with the backend only through HTTP tools.
- `yolo`: YOLOv8 training and inference. Inference stores annotated output and posts detections to the backend.

## Data flow

1. The user submits a lost item to `POST /api/lost-items`.
2. The backend persists the report and queues the investigation agent.
3. YOLO inference posts detections to `POST /api/detections` and stores an image path such as `/results/detections/image_detected.jpg`.
4. The agent calculates a weighted match score and posts qualifying matches to `POST /api/matches`.
5. Strong matches create alerts through `POST /api/alerts`.
6. The frontend reads the APIs and loads matched images through `/media/detections/...`.

The match response includes the linked detection through a SQLAlchemy relationship, so the frontend can showcase the exact image used for the match without duplicating image data in the matches table.
