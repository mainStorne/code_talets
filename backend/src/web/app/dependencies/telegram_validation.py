from fastapi import Form
import hashlib
import hmac
import json
from urllib.parse import unquote, parse_qsl
from fastapi.exceptions import HTTPException
from ..settings import settings
from ..schemas.telegram_data import TelegramData, TelegramUser
from typing import Annotated
from fastapi import Header


class TelegramInitDataAbsenceException(Exception):
    pass


class TelegramInitData:

    def __init__(self, telegram_token: str):
        self._telegram_token = telegram_token

    def __call__(self, init_data: Annotated[str, Header()]) -> TelegramData:
        if init_data is None:
            raise TelegramInitDataAbsenceException

        parsed_data = parse_qsl(init_data)
        parsed_data = dict(parsed_data)
        received_hash = parsed_data.pop('hash')
        fields = sorted(
            (key, unquote(value)) for key, value in parsed_data.items()
        )
        data_check_string = '\n'.join(f'{k}={v}' for k, v in fields)
        secret_key = hmac.new(b'WebAppData', self._telegram_token.encode(), hashlib.sha256).digest()
        computed_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        if computed_hash != received_hash:
            raise TelegramInitDataAbsenceException

        user = json.loads(parsed_data.pop('user'))

        return TelegramData(**parsed_data, user=TelegramUser(**user))


get_telegram_data = TelegramInitData(telegram_token=settings.TELEGRAM_TOKEN)
