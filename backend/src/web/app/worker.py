import logging
from .conf import connection_pool, async_session_maker, bot, settings
from .messages import ResumeMessage, CreateUserMessage
from .db.adapters.redis_client import RedisClient
from pydantic import ValidationError
import asyncio
from .utils.connect_to_api_google_sheet import init_google_sheet, writeDataToGoogleSheet

class Worker:

    async def handle_create(self, message: CreateUserMessage):

        def func():
            wks = init_google_sheet()
            writeDataToGoogleSheet(wks, message.to_list())

        # res = await asyncio.to_thread(func)
        # logging.info(res)
        try:
            func()
        except Exception as e:
            logging.error(exc_info=e, msg='')




    async def __call__(self, *args, **kwargs):
        # maybe create ping
        logging.info('start Worker')
        async with RedisClient.from_pool(connection_pool) as redis:
            async for key, payload in redis.listen(['users.create']):
                logging.info(f'recieved {key, payload}')
                if key == 'users.create':
                    logging.info('message received')
                    try:
                        message = CreateUserMessage(**payload)
                        logging.info('message received')
                        await self.handle_create(message)
                    except ValidationError as e:
                        logging.error(exc_info=e, msg='Error in worker')
