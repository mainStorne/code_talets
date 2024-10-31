from datetime import datetime

from pydantic import BaseModel, ConfigDict

class Message(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

class MessageBase(BaseModel):
    user_id: int


class UserCreateMessage(BaseModel):
    id: int
    phone_number: str
    first_name: str
    last_name: str
    middle_name: str
    age: int
    text: str
    city: str
    created_at: datetime
    telegram: str
    send_to_admin: bool = False
    status: str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def fio(self):
        return " ".join([self.last_name, self.middle_name, self.first_name])

    def to_list(self):
        # return [fio, phoneNumber, age, city, created_at, telegram]
        return [self.fio, self.phone_number, self.age, self.city, self.created_at.strftime('%H:%M:%S'), self.telegram]

from datetime import datetime
from pydantic import BaseModel, HttpUrl, model_validator, Field
from pydantic.main import IncEx


class BaseCase(Message):
    case_url: str | None
    text: str | None





class CaseCreate(BaseCase):
    executor_id: int
    exp_at: datetime



class CaseRead(CaseCreate):
    id: int



class CaseAnswer(BaseCase):
    case_url: HttpUrl | None
    text: str | None
    answer_to_id: int
    user_id: int
    created_at: datetime