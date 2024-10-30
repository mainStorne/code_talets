from time import timezone

from sqlalchemy import Integer, ForeignKey, String, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, IDMixin
from datetime import datetime


class Case(IDMixin, Base):
    __tablename__ = 'cases'
    creator: Mapped[int] = mapped_column(ForeignKey('users.id'))
    executor: Mapped[int] = mapped_column(
        ForeignKey('users.id')
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )
    exp_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )
    case_url: Mapped[str] = mapped_column(
        String(), nullable=True
    )
    text: Mapped[str] = mapped_column(
        String(), nullable=True
    )

class CaseAnswer(IDMixin, Base):
    __tablename__ = 'case_answers'
    answer_to_id: Mapped[int] = mapped_column(ForeignKey('cases.id'))
    case_url: Mapped[str] = mapped_column(
        String(), nullable=True
    )
    text: Mapped[str] = mapped_column(
        String(), nullable=True
    )


