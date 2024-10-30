from dataclasses import dataclass

@dataclass
class TelegramUser:
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str
    allows_write_to_pm: bool




@dataclass
class TelegramData:
    auth_date: str
    query_id: str
    user: TelegramUser
