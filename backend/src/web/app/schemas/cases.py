from datetime import datetime
from datetime import timezone
from typing import Literal, Any
from .users import ReadUserResume, ReadUser, ReadResume

from fastapi_sqlalchemy_toolkit import make_partial_model

from pydantic import BaseModel, HttpUrl, model_validator, Field, ConfigDict
from pydantic.main import IncEx


class BaseCase(BaseModel):
    case_url: str | None


class CaseCreate(BaseCase):
    executor_id: int
    creator_id: int | None = None
    exp_at: datetime


class CaseFile(BaseModel):
    case_url: str


class CaseRead(CaseCreate):
    creator_id: int
    id: int


CaseUpdate = make_partial_model(CaseCreate)


class CaseAnswer(BaseCase):
    answer_to_id: int
    created_at: datetime = datetime.now(tz=timezone.utc)


class CaseAnswerRead(CaseAnswer):
    id: int


CaseAnswerUpdate = make_partial_model(CaseAnswer)


class UserCaseAndAnswer(BaseModel):
    user: ReadUser = Field(validation_alias='User')
    user_resume: ReadResume = Field(validation_alias='UserResume')
    case: CaseRead  = Field(validation_alias='Case')
    case_answer: CaseAnswerRead = Field(validation_alias='CaseAnswer')
    model_config = ConfigDict(from_attributes=True)