from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    user_id: int


class ResumeMessage(MessageBase):
    text: str
    url: str


class CreateUserMessage(BaseModel):
    id: int
    phone_number: str
    first_name: str
    last_name: str
    middle_name: str
    age: int
    city: str
    created_at: datetime
    telegram: str
    status: str
    model_config = ConfigDict(arbitrary_types_allowed=True)
    @property
    def fio(self):
        return " ".join([self.last_name, self.middle_name, self.first_name])

    def to_list(self):
        # return [fio, phoneNumber, age, city, created_at, telegram]
        return [self.fio, self.phone_number, self.age, self.city, self.created_at.strftime('%H:%M:%S'), self.telegram]
