from pydantic import BaseModel

class MessageBase(BaseModel):
    user_id: int


class ResumeMessage(MessageBase):
    text: str
    url: str