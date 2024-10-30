from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.adapters.redis_client import RedisClient
from ...dependencies.session import get_session
from ...dependencies.redis import get_redis
from ...schemas.quote import QuestionRead, QuestionInput, Speciality
from ...db.models.questions import Question
from ...db.models.users import User
from ...managers.question import QuestionManager
from ...authenticator import Authenticator

r = APIRouter()
m = QuestionManager(Question)
auth = Authenticator()


@r.get('/', response_model=list[QuestionRead], dependencies=[Depends(auth.current_user())])
async def questions(session: AsyncSession = Depends(get_session)):
    return await m.list(session)  # type: ignore


@r.post('/', response_model=list[Speciality])
async def finish(questions: list[QuestionInput],
                 user: User = Depends(auth.current_user()),
                 session: AsyncSession = Depends(get_session), redis: RedisClient = Depends(get_redis)):
    response = await m.calc_results(session, questions)
    await redis.xsend(user.id, {'name'})
    return response
