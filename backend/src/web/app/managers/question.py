from .base import BaseManager as ModelManager
from sqlalchemy import select
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models.questions import Question, Speciality
from ..schemas.quote import QuestionInput
from sqlalchemy import select, func
from collections import Counter


class QuestionManager(ModelManager):

    async def calc_results(self, session: AsyncSession, questions: list[int]):
        freqs = Counter(questions)
        builder = InlineKeyboardBuilder()

        res = []

        for freq in freqs.most_common(2):
            spec = await session.get(Speciality, freq[0])
            builder.row(
                InlineKeyboardButton(
                    text=spec.name.title(),
                    callback_data=f'spec_{spec.id}'
                )
            )

            res.append(spec)

        builder.adjust(2)
        return builder.as_markup(), res

    async def questions(self, session: AsyncSession):
        sub = select(func.count(Question.id)).scalar_subquery()
        stmt = select(sub.label('total_questions'), Question)

        result = list(await session.execute(stmt))
        return result
