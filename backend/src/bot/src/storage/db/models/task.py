from sqlalchemy import Integer, ForeignKey, String, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, IDMixin
#
#
# class Task(IDMixin, Base):
#     __tablename__ = 'tasks'
#     user_id: Mapped[int] =
#     middle_name: Mapped[str] = mapped_column(
#         String(length=320)
#     )
#     last_name: Mapped[str] = mapped_column(
#         String(length=320))
#     is_superuser: Mapped[bool] = mapped_column(
#         Boolean, default=False, nullable=False
#     )
#     city: Mapped[str] =  mapped_column(
#         String(length=320))
#
#     resume_url: Mapped[str] = mapped_column(
#         String(length=800), nullable=True
#     )
#     experience: Mapped[float] = mapped_column(
#         Float
#     )
