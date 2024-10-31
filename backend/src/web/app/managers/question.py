from .base import BaseManager as ModelManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models.questions import Question, Speciality
from ..schemas.quote import QuestionInput
from sqlalchemy import select, func
from collections import Counter


class QuestionManager(ModelManager):

    async def calc_results(self, session: AsyncSession, questions:list[int]):
        freqs = Counter(questions)
        res = []

        for freq in freqs.most_common(2):
            res.append(await session.get(Speciality, freq[0]))
        # freqs = {}
        #
        # for q in questions:
        #     stmt = select(Question).join(Speciality, Speciality.id == Question.speciality_id).where(Question.id == q)
        #     q = await session.scalar(stmt)
        #     spec_id = q.speciality_id
        #     if freqs.get(spec_id, False):
        #         freqs[spec_id] = 1
        #     else:
        #         freqs[spec_id] += 1
        # most_freq = sorted(list(freqs.items()), reverse=True, key=lambda x: x[1])[:2]
        # for freq in most_freq:
        #

        return res

    async def questions(self,  session: AsyncSession):
        sub = select(func.count(Question.id)).scalar_subquery()
        stmt = select(sub.label('total_questions'), Question)

        result =  list(await session.execute(stmt))
        return result


