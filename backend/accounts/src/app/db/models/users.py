from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, IDMixin


class User(IDMixin, SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=True)
    role: Mapped['Role'] = relationship(back_populates='users', lazy='joined')