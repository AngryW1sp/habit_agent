"""Базовый класс моделей и утилиты для удобного отображения объектов."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех SQLAlchemy моделей в проекте."""

    def __repr__(self):
        """Читаемое представление модели со всеми полями и их значениями."""
        attrs = ", ".join(
            f"{k}={getattr(self, k)!r}" for k in self.__mapper__.columns.keys()
        )
        return f"{self.__class__.__name__}({attrs})"
