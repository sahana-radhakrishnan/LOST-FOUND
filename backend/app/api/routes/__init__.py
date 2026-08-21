from app.api.routes.alerts import router as alerts_router
from app.api.routes.detections import router as detections_router
from app.api.routes.lost_items import router as lost_items_router
from app.api.routes.matches import router as matches_router

__all__ = [
    "lost_items_router",
    "detections_router",
    "matches_router",
    "alerts_router",
]