from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, IDMixin


class User(IDMixin, Base):
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(length=50), unique=True, nullable=True
    )
