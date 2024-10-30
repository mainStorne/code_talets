from typing import Union

from fastapi import status
from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: Union[str, dict[str, str]]


not_a_superuser_response = {
    status.HTTP_403_FORBIDDEN: {
        "description": "Not a superuser.",
    },
}

missing_token_or_inactive_user_response = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Missing token or inactive user.",
    },
}

auth_responses = {**not_a_superuser_response, **missing_token_or_inactive_user_response}

not_found_response = {
    status.HTTP_404_NOT_FOUND: {
        'model': ErrorModel,
    }
}
