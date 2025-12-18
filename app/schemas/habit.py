"""Pydantic-схемы для сущности привычки и связанных операций."""

from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class HabitBase(BaseModel):
    """Базовая схема привычки."""

    name: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = None


class HabitCreate(HabitBase):
    """Схема для создания новой привычки."""

    pass


class HabitUpdate(BaseModel):
    """Схема для обновления полей привычки."""

    name: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = None


class HabitComplete(BaseModel):
    """Схема для отметки о выполнении привычки на конкретную дату."""

    date: date


class HabitRead(BaseModel):
    """Схема чтения привычки (ответ API)."""

    id: int
    name: str
    description: Optional[str] = None
    completed_days_count: int
    success: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
