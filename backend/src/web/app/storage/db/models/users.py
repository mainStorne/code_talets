from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, IDMixin


class User(IDMixin, Base):
    __tablename__ = 'users'
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
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(length=50), unique=True, nullable=True
    )
