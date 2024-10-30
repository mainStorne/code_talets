from datetime import datetime
from fastapi_sqlalchemy_toolkit import make_partial_model
from pydantic import BaseModel



class BaseUser(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    created_at: datetime
    age: int
    city: str
    experience: float


class CreateUser(BaseUser):
    pass

class ReadUser(BaseUser):
    id: int






UpdateUser = make_partial_model(CreateUser)