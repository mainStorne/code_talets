from datetime import datetime
from typing import Optional, TypeVar
from pydantic import EmailStr, ConfigDict, Field, BaseModel
from fastapi_users import schemas
from fastapi_users.schemas import CreateUpdateDictModel
from fastapi_sqlalchemy_toolkit import make_partial_model


class Role(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)  # type: ignore


class RoleCreate(Role):
    pass


class RoleRead(Role):
    id: int


RoleUpdate = make_partial_model(RoleCreate)


class BaseUser(CreateUpdateDictModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    role_id: int | None = None
    model_config = ConfigDict(from_attributes=True)  # type: ignore


class UserRead(BaseUser):
    id: int


class UserCreate(BaseUser):
    password: str


UserUpdate = make_partial_model(UserCreate)

UC = TypeVar('UC', bound=UserCreate)
