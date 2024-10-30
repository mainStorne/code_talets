from typing import Protocol, Coroutine, Callable, Any


class BaseAuthenticator(Protocol):

    def current_user(self, optional: bool = False,
                     active: bool = False,
                     verified: bool = False,
                     superuser: bool = False) -> Callable[[Any], Coroutine[Any, Any, Any]]:
        pass