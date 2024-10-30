from typing import Iterable, Any
from fastapi import UploadFile
from fastapi_sqlalchemy_toolkit import ModelManager
from fastapi_sqlalchemy_toolkit.model_manager import CreateSchemaT, ModelT
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models.users import UserResume
from ..schemas.users import BaseUser, CreateUser
from ..utils.save_file import save_file_to_static
from ..db.adapters.base import BaseAdapter


class UserManager(ModelManager):

    async def create_user(
        self,
        session: AsyncSession,
        id: int,
        file: UploadFile,
        in_obj: BaseUser,
        refresh_attribute_names: Iterable[str] | None = None,
        *,
        commit: bool = True,
        **attrs: Any,
    ) -> ModelT:
        file_path = save_file_to_static(file)
        user = CreateUser.model_construct(**in_obj.model_dump(), id=id, resume_url=file_path)
        return await self.create(session, user)

    async def create_resume(self, session, user_id: int, file: UploadFile):
        file_path = save_file_to_static(file)
        return await self.append_resume(session, {'user_id': user_id, 'resume_url': file_path})

    async def append_resume(self, session, data: dict):
        adapter = BaseAdapter(session, UserResume)
        return await adapter.create(data)
