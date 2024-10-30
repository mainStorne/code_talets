from .base import Base, IDMixin
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey

class Speciality(IDMixin, Base):
    __tablename__ = 'specialities'
    name: Mapped[str] = mapped_column(String(length=300))
    description: Mapped[str] = mapped_column(String)
    urls: Mapped[str] = mapped_column(String)

class Question(IDMixin, Base):
    __tablename__ = 'questions'
    name: Mapped[str] = mapped_column(String(length=300))
    speciality_id: Mapped[int] = mapped_column(ForeignKey('specialities.id'))


