from typing import Any
from venv import create

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import insert
from ...db.models.users import User
from ...db.models.roles import Role



class UserAdapter(SQLAlchemyUserDatabase[int, User]):


    async def create(self, create_dict: dict[str, Any], role: Role):
        user = self.user_table(**create_dict)
        user.role = role
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
