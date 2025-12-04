from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class HabitBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = None
    is_active: bool = True


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = None
    completed_today: Optional[bool] = None
    is_active: Optional[bool] = None


class HabitRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    completed_days_count: int
    success: bool
    completed_today: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
