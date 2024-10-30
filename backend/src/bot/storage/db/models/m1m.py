from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base import Base

from .base import IDMixin


class M1M(IDMixin, Base):
    __tablename__ = 'm1ms'
    name: Mapped[str] = mapped_column(String())
