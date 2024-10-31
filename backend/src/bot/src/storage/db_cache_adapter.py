from contextlib import asynccontextmanager

from sqlalchemy import delete, update
from typing_extensions import Generic

from .cache.redis_client import RedisClient
from .db.adapters.base import BaseAdapter
from .db.adapters.users import UserAdapter
from pydantic import BaseModel, ValidationError
from typing import TypeVar
import logging

Read = TypeVar('Read', bound=BaseModel)


class DbCacheAdapter(Generic[Read]):

    def __init__(self, get_cache, get_db, read: type[Read]):
        self.get_cache = get_cache
        self.get_db = get_db
        self._read = read

    async def _delete_handle(self, adapter: BaseAdapter, read: Read):
        stmt = delete(adapter.table).where(adapter.table.id == read.id)
        await adapter.session.execute(stmt)
        await adapter.session.commit()

    async def _create_handle(self, adapter: BaseAdapter, read: Read):
        await adapter.create(read.model_dump())

    async def _update_handle(self, adapter: BaseAdapter, read: Read):
        stmt = update(adapter.table).where(adapter.table.id == read.id).values(
            read.model_dump(exclude={'id'})
        )
        await adapter.session.execute(stmt)
        await adapter.session.commit()

    async def _handle_cud(self, cud: str, payload: dict):
        try:
            user_id = payload.pop('user_id')
            read = self._read(id=user_id, **payload)
        except ValidationError:
            return
        if cud == 'create':
            callback = self._create_handle
        elif cud == 'update':
            callback = self._update_handle
        elif cud == 'delete':
            callback = self._delete_handle
        else:
            raise

        async with asynccontextmanager(self.get_db)() as db:
            await callback(UserAdapter(db), read)

    async def listen_for_services_events(self):
        try:
            async with asynccontextmanager(self.get_cache)() as cache:
                cache: RedisClient
                async for key, payload in cache.listen_for_stream('accounts'):
                    key: str
                    _, cud = key.split('.')
                    await self._handle_cud(cud, payload)
        except Exception as e:
            logging.exception('Exception in worker task', exc_info=e)
