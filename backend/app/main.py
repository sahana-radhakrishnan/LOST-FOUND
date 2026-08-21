from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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