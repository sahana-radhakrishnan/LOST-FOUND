from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LostItemCreate(BaseModel):
    item_name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1, max_length=255)
    lost_time: datetime
    contact: str = Field(..., min_length=1, max_length=50)


class LostItemResponse(BaseModel):
    id: int
    item_name: str
    description: str
    location: str
    lost_time: datetime
    contact: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)