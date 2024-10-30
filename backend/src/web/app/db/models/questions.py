from .base import Base, IDMixin
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class Question(IDMixin, Base):
    __tablename__ = 'questions'
    name: Mapped[str] = mapped_column(String(length=300))