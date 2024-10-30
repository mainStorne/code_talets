from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, IDMixin


class User(IDMixin, Base):
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String())
    middle_name: Mapped[str] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String())
