from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject



class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, session_pool):
        self.session_pool = session_pool

    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any],
                       ) -> Any:

        event_from_user = data.get('event_from_user', None)
        if not event_from_user:
            return await handler(event, data)
        async with self.session_pool() as session:

            data["session"] = session



            result = await handler(event, data)
            return result
