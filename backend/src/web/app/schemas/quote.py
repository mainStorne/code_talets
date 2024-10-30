from pydantic import BaseModel

class BaseQuestion(BaseModel):
    name: str
    speciality_name: str


class QuestionRead(BaseQuestion):
    id: int


class QuestionInput(BaseModel):
    id: int