from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.services.media_service import image_url


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class DetectionCreate(BaseModel):
    camera_id: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=255)
    object: str = Field(..., min_length=1, max_length=100)
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime
    image_path: str = Field(..., min_length=1, max_length=500)
    bbox: BoundingBox | None = None


class DetectionResponse(BaseModel):
    id: int
    camera_id: str
    location: str
    object: str
    confidence: float
    timestamp: datetime
    image_path: str
    bbox: BoundingBox | None = None
    created_at: datetime

    @computed_field
    @property
    def image_url(self) -> str | None:
        return image_url(self.image_path)

    model_config = ConfigDict(from_attributes=True)