from fastapi_sqlalchemy_toolkit import ModelManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models.questions import Question, Speciality


class QuestionManager(ModelManager):

    async def calc_results(self, session: AsyncSession, questions: list[int]):
        res = {}
        for q in questions:
            stmt = select(Question).join(Speciality, Speciality.id == Question.speciality_id).where(Question.id == q)
            res.update(await session.scalar(stmt))


