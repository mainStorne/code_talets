import asyncio
import logging

from fastapi import Depends, WebSocket, WebSocketDisconnect
from backend.web import BaseConsumer
from backend.web import BaseProducer
from backend.infrastructure.database.repository.request import RequestRepo
from backend.web import get_repo

from backend.web import get_telegram_data
from backend.web import TelegramData
from backend.web import templates
from backend.web import AuthorizedUserAPIRouter

main_router = AuthorizedUserAPIRouter(prefix='/main')


@main_router.websocket('/')
async def ws_main(websocket: WebSocket,
                  telegram_data: TelegramData = Depends(get_telegram_data),
                  repo: RequestRepo = Depends(get_repo),
                  ):
    try:
        await websocket.accept()
        await repo.user_online_action(telegram_data.user.id)
        # need initial state for properly processing
        initial = await websocket.receive_json()
        producer = BaseProducer(websocket, telegram_data.user.id, templates)
        consumer = BaseConsumer(websocket, telegram_data.user.id, templates, initial)

        producer_task = asyncio.create_task(
            producer()
        )
        consumer_task = asyncio.create_task(
            consumer()
        )

        done, pending = await asyncio.wait((consumer_task, producer_task), return_when=asyncio.FIRST_EXCEPTION)
        for task in pending:
            task.cancel()
        for task in done:
            task.result()

        # in this direction if websocket is closed then exception WebSocketDisconnect will throw
        await websocket.close()
        await repo.user_offline_action(user_id=telegram_data.user.id)

    except WebSocketDisconnect:
        await repo.user_offline_action(user_id=telegram_data.user.id)
    except Exception as e:
        logging.error(exc_info=e, msg='Exception in websocket')
        # in this direction better first fire offline action
        await repo.user_offline_action(user_id=telegram_data.user.id)
        await websocket.close()

