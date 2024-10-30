from typing import Callable, Any, Coroutine

from .fastapi_crud_toolkit.authenticator import BaseAuthenticator
from .dependencies.user import get_current_user


class Authenticator(BaseAuthenticator):

    def current_user(self, optional: bool = False,
                           active: bool = False,
                           verified: bool = False,
                           superuser: bool = False) -> Callable[[Any], Coroutine[Any, Any, Any]]:
        return get_current_user(is_superuser=superuser)
