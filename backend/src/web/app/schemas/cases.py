from datetime import datetime
from datetime import timezone
from typing import Literal, Any

from fastapi_sqlalchemy_toolkit import make_partial_model

from pydantic import BaseModel, HttpUrl, model_validator, Field
from pydantic.main import IncEx


class BaseCase(BaseModel):
    case_url: HttpUrl | None
    text: str | None

    @model_validator(mode='after')
    def url_or_text_not_empty(self):
        if self.case_url is None and self.text is None:
            raise ValueError('Текст или url должны быть заполненны!')
        return self


class CaseCreate(BaseCase):
    creator_id: int
    executor_id: int
    start_time: datetime = datetime.now(tz=timezone.utc)
    exp_at: datetime


class CaseRead(CaseCreate):
    id: int


CaseUpdate = make_partial_model(CaseCreate)


class CaseAnswer(BaseCase):
    answer_to_id: int
    created_at: datetime


class CaseAnswerRead(CaseAnswer):
    id: int
