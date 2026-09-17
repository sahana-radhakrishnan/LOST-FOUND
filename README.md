# LOST-FOUND

AI-assisted lost-and-found investigation system. Users report lost items, YOLO detects objects from images or cameras, and the investigation agent compares detections with reports to create matches and alerts.

## Run locally

1. Start MySQL and create a database named `lost_and_found`.
2. Create `backend/.env` with `MYSQL_PASSWORD` and any required MySQL settings.
3. Install backend dependencies: `pip install -r backend/requirements.txt`.
4. Start the API from `backend`: `uvicorn app.main:app --reload --port 8001`.
5. Install frontend dependencies from `frontend`, then run `npm run dev`.
6. Open the Vite URL, normally `http://localhost:5173`.

For YOLO inference, install `pip install -r yolo/requirements.txt`, then run:

```text
python yolo/inference/detect.py path/to/image.jpg --location "Library Entrance" --camera-id CAM_03
```

The command saves annotated images to `yolo/results/detections` and registers detections through the backend API.

## Investigation flow

Submitting a lost-item report starts a background investigation. The agent retrieves detections, scores object, description, location, time, and confidence, stores the best possible match, and creates an alert for a strong match. Matched images are served by the backend under `/media`.
