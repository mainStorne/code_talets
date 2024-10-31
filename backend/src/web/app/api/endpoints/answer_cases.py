from fastapi import HTTPException, UploadFile, File, Form
from typing import Annotated
from ...dependencies.redis import get_redis
from ...db.adapters.base import BaseAdapter
from fastapi.encoders import jsonable_encoder
from ...db.adapters.redis_client import RedisClient
from ...db.models import User
from ...managers.base import BaseManager as ModelManager
from ...db.models.cases import Case, CaseAnswer as CaseAnswerDB
from ...dependencies.session import get_session
from ...authenticator import Authenticator
from ...schemas.cases import CaseCreate, CaseRead, CaseUpdate, CaseAnswer, CaseAnswerRead, CaseAnswerUpdate

from ...conf import bot

from ...utils.save_file import save_file_to_static

case_answer_manager = ModelManager(CaseAnswerDB)
auth = Authenticator()

from fastapi import Depends, Request, status, Response
from ...fastapi_crud_toolkit.crud_router import CrudRouter
from fastapi_sqlalchemy_toolkit import ModelManager
from ...fastapi_crud_toolkit.authenticator import BaseAuthenticator
from pydantic import BaseModel, ValidationError
from fastapi_users.router.common import ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession
from ...fastapi_crud_toolkit.openapi_responses import (
    not_found_response,
    missing_token_or_inactive_user_response,
    auth_responses,
    not_a_superuser_response,
    case_expired_response

)


def checker(objs: str = Form(...)):
    try:
        return CaseCreate.model_validate_json(objs)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


def get_crud_router(manager: ModelManager, get_session, read_scheme: type[BaseModel],
                    create_scheme: type[BaseModel], update_scheme: type[BaseModel],
                    authenticator: BaseAuthenticator,
                    name: str = None):
    # need a plural name
    if not name:
        name = manager.model.__tablename__
    crud = CrudRouter()
    get_current_active_user = authenticator.current_user(
        active=True
    )

    get_current_superuser = authenticator.current_user(
        active=True, superuser=True
    )

    @crud.get('/', response_model=list[read_scheme], name=f'{name}:all',
              dependencies=[Depends(get_current_active_user)],
              responses={**missing_token_or_inactive_user_response})
    async def objs(request: Request, session: AsyncSession = Depends(get_session), ):
        return await manager.list(session)

    @crud.patch("/{id}", response_model=read_scheme, responses={
        **auth_responses,
        **not_found_response,
    }, name=f'{name}:patch one',
                dependencies=[Depends(get_current_superuser)])
    async def obj(request: Request, id: int, scheme: update_scheme, session: AsyncSession = Depends(get_session)):
        model = await manager.get_or_404(session, id=id)
        return await manager.update(session, model, scheme)

    @crud.get("/{id}",
              dependencies=[Depends(get_current_active_user)],
              response_model=read_scheme,
              responses={
                  **missing_token_or_inactive_user_response,
                  **not_found_response
              },
              name=f'{name}:one',
              )
    async def obj(request: Request, id: int, session: AsyncSession = Depends(get_session)):
        return await manager.get_or_404(session, id=id)

    # @crud.post("/", response_model=read_scheme, responses={
    #     **missing_token_or_inactive_user_response,
    #     status.HTTP_409_CONFLICT: {
    #         "model": ErrorModel,
    #     }
    # }, status_code=status.HTTP_201_CREATED, name=f"{name}:new one",
    #
    #            )
    # async def obj(objs: create_scheme = Depends(checker), file: UploadFile | None = None,
    #               session: AsyncSession = Depends(get_session)
    #               , user: User = Depends(get_current_active_user), redis: RedisClient = Depends(get_redis)):
    #     objs.creator_id = user.id
    #     if objs.case_url is None:
    #         path = save_file_to_static(file)
    #         objs.case_url = path
    #
    #     response = await manager.create(session, objs)
    #     await redis.xadd('users.cases.create',
    #                      {'id': response.id, 'exp_at': objs.exp_at.timestamp(), **objs.model_dump(exclude={'exp_at'})})
    #     return response

    @crud.delete("/{id}",
                 dependencies=[Depends(get_current_superuser)],
                 response_class=Response,
                 responses={
                     **auth_responses,
                     **not_found_response
                 }, status_code=status.HTTP_204_NO_CONTENT, name=f'{name}:delete one')
    async def obj(request: Request, id: int, session: AsyncSession = Depends(get_session)):
        obj_in_db = await manager.get_or_404(session, id=id)
        await manager.delete(session, obj_in_db)
        return

    return crud


r = get_crud_router(case_answer_manager, get_session,
                    CaseAnswerRead, CaseAnswerUpdate, CaseAnswer,
                    auth,
                    )
