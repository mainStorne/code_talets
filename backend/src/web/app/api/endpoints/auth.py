from typing import Tuple, Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import models
from fastapi_users.authentication import AuthenticationBackend, Authenticator, Strategy
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel
from typing_extensions import Doc


class OAuth2PasswordRequestBody:
    def __init__(
            self,
            *,
            grant_type: Annotated[
                Union[str, None],
                Form(pattern="password"),
                Doc(
                    """
                    The OAuth2 spec says it is required and MUST be the fixed string
                    "password". Nevertheless, this dependency class is permissive and
                    allows not passing it. If you want to enforce it, use instead the
                    `OAuth2PasswordRequestFormStrict` dependency.
                    """
                ),
            ] = None,
            username: Annotated[
                str,
                Form(),
                Doc(
                    """
                    `username` string. The OAuth2 spec requires the exact field name
                    `username`.
                    """
                ),
            ],
            password: Annotated[
                str,
                Form(),
                Doc(
                    """
                    `password` string. The OAuth2 spec requires the exact field name
                    `password".
                    """
                ),
            ],
            scope: Annotated[
                str,
                Form(),
                Doc(
                    """
                    A single string with actually several scopes separated by spaces. Each
                    scope is also a string.

                    For example, a single string with:

                    ```python
                    "items:read items:write users:read profile openid"
                    ````

                    would represent the scopes:

                    * `items:read`
                    * `items:write`
                    * `users:read`
                    * `profile`
                    * `openid`
                    """
                ),
            ] = "",
            client_id: Annotated[
                Union[str, None],
                Form(),
                Doc(
                    """
                    If there's a `client_id`, it can be sent as part of the form fields.
                    But the OAuth2 specification recommends sending the `client_id` and
                    `client_secret` (if any) using HTTP Basic auth.
                    """
                ),
            ] = None,
            client_secret: Annotated[
                Union[str, None],
                Form(),
                Doc(
                    """
                    If there's a `client_password` (and a `client_id`), they can be sent
                    as part of the form fields. But the OAuth2 specification recommends
                    sending the `client_id` and `client_secret` (if any) using HTTP Basic
                    auth.
                    """
                ),
            ] = None,
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


def get_auth_router(
    backend: AuthenticationBackend[models.UP, models.ID],
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    authenticator: Authenticator[models.UP, models.ID],
    requires_verification: bool = False,
) -> APIRouter:
    """Generate a router with login/logout routes for an authentication backend."""
    router = APIRouter()
    get_current_user_token = authenticator.current_user_token(
        active=True, verified=requires_verification
    )

    login_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LOGIN_BAD_CREDENTIALS: {
                            "summary": "Bad credentials or the user is inactive.",
                            "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                        },
                        ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                            "summary": "The user is not verified.",
                            "value": {"detail": ErrorCode.LOGIN_USER_NOT_VERIFIED},
                        },
                    }
                }
            },
        },
        **backend.transport.get_openapi_login_responses_success(),
    }

    @router.post(
        "/login",
        name=f"auth:{backend.name}.login",
        responses=login_responses,
    )
    async def login(
        request: Request,
        credentials: OAuth2PasswordRequestForm = Depends(),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
        strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
    ):
        user = await user_manager.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        if requires_verification and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
            )
        response = await backend.login(strategy, user)
        await user_manager.on_after_login(user, request, response)
        return response

    logout_responses: OpenAPIResponseType = {
        **{
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user."
            }
        },
        **backend.transport.get_openapi_logout_responses_success(),
    }

    @router.post(
        "/logout", name=f"auth:{backend.name}.logout", responses=logout_responses
    )
    async def logout(
        user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
        strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
    ):
        user, token = user_token
        return await backend.logout(strategy, user, token)

    return router