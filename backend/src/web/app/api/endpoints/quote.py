from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from ...dependencies.session import get_session
from ...schemas.quote import QuestionRead, QuestionInput
from fastapi_sqlalchemy_toolkit import ModelManager
from ...db.models.questions import Question


r = APIRouter()
m = ModelManager(Question)


@r.get('/', response_model=list[QuestionRead])
async def questions(session: AsyncSession = Depends(get_session)):
    return await m.list(session)  # type: ignore

@r.post('/')
async def finish(questions: list[QuestionInput], session: AsyncSession = Depends(get_session)):
    pass