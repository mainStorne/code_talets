from typing import Annotated

from fastapi import APIRouter, Form, Request, Depends, HTTPException
from backend.infrastructure.database.repository.request import RequestRepo
from backend.web import get_repo
from backend.web import get_telegram_data
from backend.web import TelegramData
from backend.web import templates

chats_router = APIRouter(prefix='/chats')


@chats_router.get('/')
async def chats(request: Request,
                repo: RequestRepo = Depends(get_repo),
                telegram_data: TelegramData = Depends(get_telegram_data),
                ):
    # get here all chats and then handler handle these chats and give data for this chats
    await repo.redis.fire_action(telegram_data.user.id, {'is_stuff': 1, 'type': 'chat_list'})
    recent_chats = await repo.chats.recent_chats_and_message(telegram_data.user.id)
    return templates.TemplateResponse(request=request, name='chats/chats.html', context={'recent_chats': recent_chats})


@chats_router.get('/search')
async def search_for_chat(request: Request,
                          q: Annotated[str, Form()],
                          skip: Annotated[int, Form()],
                          limit: Annotated[int, Form()],
                          template: Annotated[str, Form()],
                          repo: RequestRepo = Depends(get_repo),

                          telegram_data: TelegramData = Depends(get_telegram_data)):
    found_chats = await repo.chats.search_chat(telegram_data.user.id, q, skip, limit)
    return templates.TemplateResponse(request=request, name=template,
                                      context={'found_chats': found_chats})


# maybe create group chat event or redis
@chats_router.get('/private/{user_id}')
async def private_chat(request: Request,
                       user_id: int,
                       repo: RequestRepo = Depends(get_repo),
                       telegram_data: TelegramData = Depends(get_telegram_data),
                       ):
    # maybe can send chat_id if exists
    if telegram_data.user.id == user_id:
        # handle this ?
        raise HTTPException(status_code=404)
    # TODO check all routes in everyone can show users this is a bad design! get rights (roles, permissions)
    # handle user id
    user = await repo.user.get_user(user_id)

    chat = await repo.chats.get_private_chat(user.id, telegram_data.user.id)
    if chat is None:
        messages = []
    else:
        messages = await repo.message.get_messages_from_chat(chat.id)

    result = await repo.redis.fire_action(telegram_data.user.id,
                                          {'is_stuff': 1, 'type': 'private_chat', 'second_user_id': user.id})
    return templates.TemplateResponse(request=request, name='chats/private-chat.html',
                                      context={'user': user, 'messages': messages, 'chat': chat})
