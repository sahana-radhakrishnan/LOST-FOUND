Base URL: `http://127.0.0.1:8001`

## Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Health check |
| GET, POST | `/api/lost-items` | List or create lost-item reports |
| GET | `/api/lost-items/{id}` | Retrieve one lost item |
| GET, POST | `/api/detections` | List or register YOLO detections |
| GET | `/api/detections/{id}` | Retrieve one detection |
| GET, POST | `/api/matches` | List or create matches |
| GET | `/api/matches/{id}` | Retrieve one match and its detection image path |
| GET, POST | `/api/alerts` | List or create alerts |
| GET | `/media/{path}` | Serve YOLO result images |

## Detection payload

```json
{
	"camera_id": "CAM_03",
	"location": "Library Entrance",
	"object": "backpack",
	"confidence": 0.94,
	"timestamp": "2026-08-20T15:30:00",
	"image_path": "/results/detections/image_detected.jpg"
}
```

The frontend converts the stored `/results/...` path to `/media/...` using the backend base URL.
