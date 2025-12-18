"""Модели SQLAlchemy для сущностей habit и habit_checkin."""

from datetime import datetime, date
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.models.base import Base


class Habit(Base):
    """Модель привычки."""

    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed_days_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    checkins: Mapped[list["HabitCheckin"]] = relationship(
        back_populates="habit", cascade="all, delete-orphan"
    )

    @hybrid_property
    def success(self) -> bool:
        """Возвращает True, если выполнений привычки >= 21 (успех)."""
        return self.completed_days_count >= 21

    __table_args__ = (Index("ix_habits_is_active", "is_active"),)


class HabitCheckin(Base):
    """Запись о выполнении привычки на конкретную дату."""

    __tablename__ = "habit_checkins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    habit = relationship("Habit", back_populates="checkins")

    __table_args__ = (
        UniqueConstraint("habit_id", "date"),
        Index("ix_checkins_habit_date", "habit_id", "date"),
    )
