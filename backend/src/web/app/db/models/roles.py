from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, IDMixin

class Role(IDMixin, Base):
    __tablename__ = 'roles'
    name: Mapped[str] = mapped_column(String(length=50), unique=True, nullable=False)
    users: Mapped[list['User']] = relationship(back_populates='role')