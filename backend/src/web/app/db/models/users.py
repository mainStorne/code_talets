from datetime import datetime
from operator import length_hint

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import SmallInteger, ForeignKey, String, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, IDMixin


class User(IDMixin, Base):
    __tablename__ = 'users'
    phone_number: Mapped[int] = mapped_column(String(length=20))
    first_name: Mapped[str] = mapped_column(
        String(length=320)
    )
    middle_name: Mapped[str] = mapped_column(
        String(length=320)
    )
    last_name: Mapped[str] = mapped_column(
        String(length=320))
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    age: Mapped[int] = mapped_column(SmallInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    city: Mapped[str] = mapped_column(
        String(length=320))

    work_experience: Mapped[str] = mapped_column(
        String(length=300)
    )

    status: Mapped[str] = mapped_column(String(length=50), nullable=True)
    resumes: Mapped[list['UserResume']] = relationship(back_populates='user', cascade='all, delete')



class UserResume(IDMixin, Base):
    __tablename__ = 'user_resumes'
    resume_url: Mapped[str] = mapped_column(String(length=500))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(back_populates='resumes', cascade='all, delete')
