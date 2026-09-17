from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.detection import DetectionResponse


class MatchCreate(BaseModel):
    lost_item_id: int = Field(..., gt=0)
    detection_id: int = Field(..., gt=0)
    match_score: float = Field(..., ge=0.0, le=1.0)
    decision: str = Field(..., min_length=1, max_length=50)
    reason: str = Field(..., min_length=1)


class MatchResponse(BaseModel):
    id: int
    lost_item_id: int
    detection_id: int
    match_score: float
    decision: str
    reason: str
    status: str
    created_at: datetime
    detection: DetectionResponse | None = None

    model_config = ConfigDict(from_attributes=True)