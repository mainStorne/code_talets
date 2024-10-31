from pydantic import BaseModel, ConfigDict

class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
    allows_write_to_pm: bool
    model_config = ConfigDict(arbitrary_types_allowed=True)




class TelegramData(BaseModel):
    auth_date: str
    query_id: str
    user: TelegramUser
