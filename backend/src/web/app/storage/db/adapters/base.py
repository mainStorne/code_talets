from typing import Generic, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_sqlalchemy_toolkit.model_manager import ModelT


class BaseAdapter(Generic[ModelT]):
    session: AsyncSession

    def __init__(
            self,
            session: AsyncSession,
            user_table: type[ModelT],
    ):
        self.session = session
        self.table = user_table

    async def create(self, create_dict: dict[str, Any]) -> ModelT:
        user = self.table(**create_dict)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, model: ModelT, update_dict: dict[str, Any]) -> ModelT:
        for key, value in update_dict.items():
            setattr(model, key, value)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def delete(self, model: ModelT) -> None:
        await self.session.delete(model)
        await self.session.commit()
