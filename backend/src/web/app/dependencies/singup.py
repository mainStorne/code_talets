from fastapi import Depends, Request
from backend.infrastructure.database.models.users import User
from .user import get_user


class UserExistException(Exception):
    pass


class UserDoesntExistException(Exception):
    pass

class UserDoesntExistGlobalDependency:
    """
    if user exists it means, he doesn't need to register again!
    """

    def __call__(self, request: Request, user: User | None = Depends(get_user)) -> None:
        if user is not None:
            raise UserExistException





class UserExistsGlobalDependency:
    """
    if user exists it means, he doesn't need to register again!
    """

    def __call__(self, user: User | None = Depends(get_user)) -> None:
        if user is None:
            raise UserDoesntExistException