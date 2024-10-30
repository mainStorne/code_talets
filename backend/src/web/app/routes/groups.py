from typing import Annotated
from fastapi import APIRouter, Form, Request, Depends
from backend.web import templates
from backend.infrastructure.database.repository.request import RequestRepo
from backend.web import get_repo

groups_router = APIRouter(prefix='/groups')


@groups_router.post('/get_group_branches/')
async def get_group_branches(request: Request,
                             group_id: Annotated[int, Form()],
                             repo: RequestRepo = Depends(get_repo)):
    pass


@groups_router.post('/search/')
async def search_for_group(request: Request,
                           template: Annotated[str, Form()],
                           skip: Annotated[int, Form()],
                           limit: Annotated[int, Form()],
                           q: Annotated[str | None, Form()] = None,
                           repo: RequestRepo = Depends(get_repo)):
    if q is None:
        guessed_groups = await repo.group.get_groups(skip, limit)
    else:
        guessed_groups = await repo.group.search_for_group(q, skip, limit)
    return templates.TemplateResponse(request=request, name=template,
                                      context={'groups_and_branches': guessed_groups})


@groups_router.get('/role/')
async def get_group():
    pass
