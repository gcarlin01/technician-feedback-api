from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


Mood = Literal["frustrated", "neutral", "positive"]
Priority = Literal["low", "normal", "high"]
FeedbackStatus = Literal["new", "in_progress", "resolved"]


class FeedbackFields(BaseModel):
    model_config = ConfigDict(extra="forbid")

    technician_name: str = Field(min_length=1, max_length=120)
    feedback_text: str = Field(min_length=1, max_length=5000)
    score: Optional[int] = Field(default=None, ge=1, le=5)
    mood: Optional[Mood] = None
    assigned_team: Optional[str] = Field(default=None, max_length=120)
    priority: Priority = "normal"
    status: FeedbackStatus = "new"


class FeedbackCreate(FeedbackFields):
    pass


class FeedbackUpdate(FeedbackFields):
    pass


class FeedbackRead(FeedbackFields):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid")
