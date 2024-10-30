from pydantic import BaseModel

class BaseQuestion(BaseModel):
    name: str
    speciality_id: int


class QuestionRead(BaseQuestion):
    id: int


class QuestionInput(BaseModel):
    id: int

class Speciality(BaseModel):
    id: int
    name: str
    text: str
    urls: str