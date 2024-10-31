from datetime import datetime
from datetime import timezone
from typing import Literal, Any

from fastapi_sqlalchemy_toolkit import make_partial_model

from pydantic import BaseModel, HttpUrl, model_validator, Field
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