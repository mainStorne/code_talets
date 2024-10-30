from fastapi_users.exceptions import FastAPIUsersException
from enum import StrEnum

class RoleDoesntExist(FastAPIUsersException):
    pass


class ErrorCodes(StrEnum):
    ROLE_DOESNT_EXIST = 'ROLE_DOESNT_EXITS'
