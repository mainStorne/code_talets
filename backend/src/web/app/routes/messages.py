from typing import Annotated

from fastapi import Request, Depends, HTTPException, Form
from backend.infrastructure.database.repository.request import RequestRepo
from backend.infrastructure.database.models import User, Message
from backend.web import get_repo
from backend.web import get_telegram_data
from backend.web import TelegramData
from backend.web import templates
from backend.web import AuthorizedUserAPIRouter

messages_router = AuthorizedUserAPIRouter(prefix='/messages')


@messages_router.get('/')
async def recent_messages(request: Request,
                          repo: RequestRepo = Depends(get_repo),
                          telegram_data: TelegramData = Depends(get_telegram_data),
                          ):
    recent_chats = await repo.message.unread_user_messages(telegram_data.user.id)
    return templates.TemplateResponse(request=request, name='messages/messages.html',
                                      context={'recent_chats': recent_chats})


@messages_router.get('/search')
async def search(request: Request,
                 q: Annotated[str, Form()],
                 skip: Annotated[int, Form()],
                 limit: Annotated[int, Form()],
                 template: Annotated[str, Form()],
                 repo: RequestRepo = Depends(get_repo),
                 telegram_data: TelegramData = Depends(get_telegram_data)
                 ):
    found_messages = await repo.message.ilike_search(telegram_data.user.id, q, skip, limit)
    return templates.TemplateResponse(request=request, name=template,
                                      context={'found_messages': found_messages})


@messages_router.get('/{message_id}/')
async def answer_to_private_message(request: Request,
                                    message_id: int,
                                    repo: RequestRepo = Depends(get_repo),
                                    telegram_data: TelegramData = Depends(get_telegram_data),
                                    ):
    # this route assumes that uses enters to other's message
    # TODO check all routes in everyone can show users this is a bad design! get rights (roles, permissions)
    message = await repo.session.get(Message, message_id)
    if message is None:
        raise HTTPException(status_code=404)
    #
    if message.sender_id == telegram_data.user.id:
        raise HTTPException(status_code=404)

    chat = await repo.chats.get_chat_from_message(message.id)
    user = await repo.session.get(User, message.sender_id)

    return templates.TemplateResponse(request=request, name='messages/answer_to_private_message.html',
                                      context={'user': user, 'message': message, 'chat': chat})
