from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AlertCreate(BaseModel):
    match_id: int = Field(..., gt=0)
    alert_type: str = Field(..., min_length=1, max_length=50)
    message: str = Field(..., min_length=1)
    status: str = Field(default="PENDING", min_length=1, max_length=50)


class AlertResponse(BaseModel):
    id: int
    match_id: int
    alert_type: str
    message: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)