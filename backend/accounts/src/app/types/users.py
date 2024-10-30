from typing import Protocol, TypeVar


class UserProtocol(Protocol):
    """User protocol that ORM model should follow."""

    id: int
    username: str
    email: str | None


UserType = TypeVar("UserType", bound=UserProtocol)