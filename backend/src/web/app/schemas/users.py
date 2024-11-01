from datetime import datetime
from fastapi_sqlalchemy_toolkit import make_partial_model

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal
from .resumes import ResumeRead

class BaseUser(BaseModel):
    first_name: str
    middle_name: str
    phone_number: str
    last_name: str
    created_at: datetime = datetime.now()
    is_superuser: bool = False
    age: int = Field(le=200, ge=13)
    city: str
    status: Literal['хороший кандидат', 'отличный', 'не подходит'] | None = None
    work_experience: str

class CreateUser(BaseUser):
    pass


class ReadUser(BaseUser):
    id: int


class ReadUserResume(ReadUser):
    resume: ResumeRead | None

class ReadResume(BaseModel):
    id: int
    resume_url: str
    user_id: int


UpdateUser = make_partial_model(CreateUser)
