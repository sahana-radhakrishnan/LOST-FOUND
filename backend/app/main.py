from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy import text

from app import models  # noqa: F401
from app.api.routes import (
    alerts_router,
    detections_router,
    lost_items_router,
    matches_router,
)
from app.database.config import settings
from app.database.session import Base, engine


# Create database tables.
Base.metadata.create_all(bind=engine)

with engine.begin() as connection:

    try:
        connection.execute(text("ALTER TABLE detections ADD COLUMN bbox JSON NULL"))
    except Exception:
        pass


app = FastAPI(
    title="Lost & Found Investigation Agent API",
    description="Backend API for the Lost & Found Investigation Agent.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

app.include_router(
    lost_items_router,
    prefix="/api",
)

app.include_router(
    detections_router,
    prefix="/api",
)

app.include_router(
    matches_router,
    prefix="/api",
)

app.include_router(
    alerts_router,
    prefix="/api",
)

YOLO_RESULTS_DIR = Path(__file__).resolve().parents[2] / "yolo" / "results"
YOLO_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=YOLO_RESULTS_DIR), name="media")