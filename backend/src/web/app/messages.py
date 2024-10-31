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
        return " ".join([self.last_name.title(), self.middle_name.title(), self.first_name.title()])

    def to_list(self):
        return [self.fio, self.phone_number, self.age, self.city.title(), self.created_at.strftime('%d.%B.%Y %H:%M:%S'), self.telegram, self.status]
