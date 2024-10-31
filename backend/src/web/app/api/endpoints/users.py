from http.client import HTTPException

from fastapi_sqlalchemy_toolkit import ModelManager

from ...db.models import UserResume
from ...dependencies.session import get_session
from ...authenticator import Authenticator
from ...schemas.users import UpdateUser, BaseUser, ReadUser, ReadUserResume
from ...conf import bot
from ...db.models.users import User

m = ModelManager(User)
m_resume = ModelManager(UserResume)
auth = Authenticator()

from fastapi import Depends, Request, status, Response
from sqlalchemy.orm import joinedload
from ...fastapi_crud_toolkit.crud_router import CrudRouter
from fastapi_sqlalchemy_toolkit import ModelManager
from ...fastapi_crud_toolkit.authenticator import BaseAuthenticator
from pydantic import BaseModel
from fastapi_users.router.common import ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession
from ...fastapi_crud_toolkit.openapi_responses import (
    not_found_response,
    missing_token_or_inactive_user_response,
    auth_responses,
    not_a_superuser_response,
    case_expired_response

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
              response_model=ReadUserResume,
              responses={
                  **missing_token_or_inactive_user_response,
                  **not_found_response
              },
              name=f'{name}:one',
              )
    async def obj(request: Request, id: int, session: AsyncSession = Depends(get_session)):
        return await manager.get_or_404(session, id=id, options=joinedload(User.resume))

    @crud.delete("/{id}",
                 # dependencies=[Depends(get_current_superuser)],
                 response_class=Response,
                 responses={
                     **auth_responses,
                     **not_found_response
                 }, status_code=status.HTTP_204_NO_CONTENT, name=f'{name}:delete one')
    async def obj(request: Request, id: int, session: AsyncSession = Depends(get_session)):
        obj_in_db = await manager.get_or_404(session, id=id, options=joinedload(User.resume))
        await manager.delete(session, obj_in_db)
        return

    # async def upload():
    #     pass
    return crud


r = get_crud_router(m,
                    get_session,
                    ReadUser, BaseUser, UpdateUser,
                    auth)
