from fastapi import Form
from typing import Annotated


class UserDoesntKnowHisRoleException(Exception):
    pass


def get_role_id(role_id: int = None, role_id_form: Annotated[int | None, Form(alias='role_id')] = None):
    """
    get user role id from web client
    """
    user_role = role_id if role_id else role_id_form
    # if user_role is None:
    #     raise UserDoesntKnowHisRoleException
    return user_role
