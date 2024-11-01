from warnings import simplefilter

from .base import BaseManager
from sqlalchemy import select
from ..db.models.users import User, UserResume
from ..db.models.cases import Case, CaseAnswer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class CaseManager(BaseManager):
    async def get_user_case(self, session: AsyncSession, answer_case_id: int):

        stmt = (select(CaseAnswer, User, UserResume, Case)
                .join(Case, Case.id == CaseAnswer.answer_to_id)

                .join(User, User.id == Case.executor_id)
                .join(UserResume, User.id == UserResume.user_id)
                .where(CaseAnswer.id == answer_case_id)
                )

        return (await session.execute(stmt)).mappings().one()
