from datetime import datetime
from fastapi_sqlalchemy_toolkit import make_partial_model

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class BaseUser(BaseModel):
    first_name: str
    middle_name: str
    phone_number: str
    last_name: str
    created_at: datetime = datetime.now()
    is_superuser: bool = False
    age: int = Field(le=200, ge=13)
    city: str
    status: Literal['хороший кондидат', 'отличный', 'не подходит'] | None = None
    work_experience: str

class CreateUser(BaseUser):
    pass


class ReadUser(BaseUser):
    id: int


UpdateUser = make_partial_model(CreateUser)
