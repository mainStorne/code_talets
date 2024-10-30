from fastapi_sqlalchemy_toolkit import ModelManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models.questions import Question, Speciality
from ..schemas.quote import QuestionInput


class QuestionManager(ModelManager):

    async def calc_results(self, session: AsyncSession, questions:list[QuestionInput]):
        freqs = {}

        for q in questions:
            stmt = select(Question).join(Speciality, Speciality.id == Question.speciality_id).where(Question.id == q.id)
            q = await session.scalar(stmt)
            spec_id = q.speciality_id
            if freqs.get(spec_id, False):
                freqs[spec_id] = 1
            else:
                freqs[spec_id] += 1
        most_freq = sorted(list(freqs.items()), reverse=True, key=lambda x: x[1])[:2]
        res = []
        for freq in most_freq:
            res.append(await session.get(Speciality, freq[0]))

        return res
