from datetime import datetime
from datetime import timezone
from fastapi_sqlalchemy_toolkit import make_partial_model

from pydantic import BaseModel, HttpUrl, model_validator

class CaseBase(BaseModel):
    start_time: datetime = datetime.now(tz=timezone.utc)
    exp_at: datetime
    url: HttpUrl | None
    text: str | None

    @model_validator(mode='after')
    def url_or_text_not_empty(self):
        if self.url is None and self.text is None:
            raise ValueError('Текст или url должны быть заполненны!')
        return self



class CaseRead(CaseBase):
    id: int



CaseUpdate = make_partial_model(CaseBase)