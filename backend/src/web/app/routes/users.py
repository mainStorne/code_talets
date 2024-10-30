from typing import Annotated
from fastapi import Form, Request, Depends
from backend.infrastructure.database.repository.request import RequestRepo
from backend.web import get_role_id
from backend.web import get_repo
from backend.web import get_telegram_data
from backend.web import TelegramData
from backend.web.src.app.utils.authorized_user_router import AuthorizedUserAPIRouter
from backend.web.src.app.utils import templates

users_router = AuthorizedUserAPIRouter(prefix='/users')


async def teacher_profile(request: Request,
                          telegram_data: TelegramData,
                          repo: RequestRepo):
    # teacher_from_redis = # await redis.get('')
    # if not teacher_from_redis:

    joined_teacher_and_user = await repo.teacher.get_joined_teacher(teacher_id=telegram_data.user.id)
    if not joined_teacher_and_user:
        return templates.TemplateResponse(request=request, name='partials/msgs/warning-msg.html',
                                          context={'msgs': ('Вы не являетесь учителем!',)},
                                          headers={'HX-Retarget': '#dynamic-msgs', 'HX-Reswap': 'innerHTML'})

    joined_teacher, joined_user = joined_teacher_and_user
    return templates.TemplateResponse(request=request, name='profiles/teacher-profile.html',
                                      context={'user': joined_user, 'teacher': joined_teacher})


async def student_profile(request: Request,
                          telegram_data: TelegramData,
                          repo: RequestRepo):
    # teacher_from_redis = # await redis.get('')
    # if not teacher_from_redis:
    joined_student_and_user = await repo.student.get_joined_student(student_id=telegram_data.user.id)
    if not joined_student_and_user:
        return templates.TemplateResponse(request=request, name='partials/msgs/warning-msg.html',
                                          context={'msgs': ('Вы не являетесь студентом!',)},
                                          headers={'HX-Retarget': '#dynamic-msgs', 'HX-Reswap': 'innerHTML'})

    joined_student, joined_user = joined_student_and_user
    return templates.TemplateResponse(request=request, name='profiles/student-profile.html',
                                      context={'user': joined_user, 'student': joined_student})


@users_router.get('/me')
async def me(request: Request,
             telegram_data: TelegramData = Depends(get_telegram_data),
             role_id: int = Depends(get_role_id),
             repo: RequestRepo = Depends(get_repo)):
    user = await repo.user.get_user(telegram_data.user.id)
    return templates.TemplateResponse(request=request, name='users/me.html', context={'user': user})

    # role = await repo.role.get_role(role_id)
    # if role.name == 'teacher':
    #     return await teacher_profile(request, telegram_data, repo)
    # elif role.name == 'student':
    #     return await student_profile(request, telegram_data, repo)


@users_router.post('/search/')
async def find_users(request: Request,
                     q: Annotated[str, Form()],
                     skip: Annotated[int, Form()],
                     limit: Annotated[int, Form()],
                     template: Annotated[str, Form()],
                     role_id: int = Depends(get_role_id),
                     telegram_data: TelegramData = Depends(get_telegram_data),
                     repo: RequestRepo = Depends(get_repo),
                     ):
    # TODO permissions!
    # if len(view_roles_id) == 3:
    # if user have all privileges on view users
    # pass
    # personal_permissions = await repo.user.get_personal_user_permissions(telegram_data.user.id)

    found_users_and_roles = await repo.user.search_for(telegram_data.user.id, q, skip, limit)
    return templates.TemplateResponse(request=request, name=template,
                                      context={'users': found_users_and_roles})
