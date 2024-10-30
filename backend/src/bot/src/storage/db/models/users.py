from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, IDMixin


class User(IDMixin, Base):
    __tablename__ = 'users'
    first_name: Mapped[str] = mapped_column(String())
    middle_name: Mapped[str] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String())


