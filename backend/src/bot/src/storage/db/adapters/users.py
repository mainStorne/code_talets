from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseAdapter
from ..models.users import User


class UserAdapter(BaseAdapter[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
