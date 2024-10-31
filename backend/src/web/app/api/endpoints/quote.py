from typing import Annotated

from fastapi import APIRouter, Depends, Response, status, Body
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from ...db.adapters.redis_client import RedisClient
from ...dependencies.session import get_session
from ...dependencies.redis import get_redis
from ...schemas.quote import QuestionRead, QuestionInput, Speciality, QuestionOutput
from ...db.models.questions import Question
from ...db.models.users import User
from ...managers.question import QuestionManager
from ...authenticator import Authenticator
from ...conf import bot

r = APIRouter()
m = QuestionManager(Question)
auth = Authenticator()


@r.get('/', dependencies=[Depends(auth.current_user())])
async def questions(session: AsyncSession = Depends(get_session)) -> Page[QuestionRead]:
    return await m.paginated_list(session)  # type: ignore


@r.post('/', response_model=list[Speciality])
async def finish(spec_ids: Annotated[list[int], Body(embeded=True)],
                 user: User = Depends(auth.current_user()),
                 session: AsyncSession = Depends(get_session)):
    markup, response = await m.calc_results(session, spec_ids)

    # Настраиваем размер клавиатуры
    await bot.send_message(user.id, f'🎉Вы Успешно прошли тест!🎉\n\n Выберите полученные специальности:',
                           reply_markup=markup)
    return response
