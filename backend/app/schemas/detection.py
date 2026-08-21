from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DetectionCreate(BaseModel):
    camera_id: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=255)
    object: str = Field(..., min_length=1, max_length=100)
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime
    image_path: str = Field(..., min_length=1, max_length=500)


class DetectionResponse(BaseModel):
    id: int
    camera_id: str
    location: str
    object: str
    confidence: float
    timestamp: datetime
    image_path: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)