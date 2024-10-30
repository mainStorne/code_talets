from pydantic import BaseModel
class BaseLifespan(BaseModel):
    next_url: str | None = None



class Lifespan1(BaseLifespan):
    first_name: str
    middle_name: str
    last_name: str


