from .base import Base, IDMixin
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey

class Speciality(IDMixin, Base):
    __tablename__ = 'specialities'
    name: Mapped[str] = mapped_column(String(length=300))
    text: Mapped[str] = mapped_column(String)
    urls: Mapped[str] = mapped_column(String)
    questions: Mapped['Question'] = relationship(back_populates='speciality')

class Question(IDMixin, Base):
    __tablename__ = 'questions'
    name: Mapped[str] = mapped_column(String(length=300))
    speciality_id: Mapped[int] = mapped_column(ForeignKey('specialities.id'))
    speciality: Mapped['Speciality'] = relationship(back_populates='questions')



