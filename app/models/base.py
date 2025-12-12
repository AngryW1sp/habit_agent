from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self):
        attrs = ", ".join(
            f"{k}={getattr(self, k)!r}"
            for k in self.__mapper__.columns.keys()
        )
        return f"{self.__class__.__name__}({attrs})"
