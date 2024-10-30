from datetime import datetime
from fastapi_sqlalchemy_toolkit import make_partial_model

from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    created_at: datetime = datetime.now()
    is_superuser: bool = False
    age: int = Field(le=200, ge=13)
    city: str
    work_experience: str


class CreateUser(BaseUser):
    pass


class ReadUser(BaseUser):
    id: int


UpdateUser = make_partial_model(CreateUser)
