from enum import Enum
from typing import Annotated, Callable, Coroutine, Any, Optional, List, Sequence, Union, Type, Dict
from fastapi import APIRouter, Request, Depends, Response, params, status
from fastapi.datastructures import Default
from fastapi.routing import APIRoute
from fastapi.utils import generate_unique_id
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute
from starlette.types import Lifespan, ASGIApp
from typing_extensions import Doc  # type: ignore

from backend.web.src.app.dependencies.singup import UserExistsGlobalDependency, UserExistException, UserDoesntExistException, \
    UserDoesntExistGlobalDependency


class UserExistsAPIRoute(APIRoute):

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            app = request.app
            try:
                return await original_route_handler(request)
            except UserDoesntExistException:
                return Response(headers={'HX-Redirect': '/signup/'})

        return custom_route_handler


class UserDoesntExistAPIRoute(APIRoute):

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            app = request.app
            try:
                return await original_route_handler(request)
            except UserExistException:
                return Response(headers={'HX-Location': '/chats/'}, status_code=status.HTTP_204_NO_CONTENT)

        return custom_route_handler


class NonAuthorizedUserAPIRouter(APIRouter):
    def __init__(self,
                 *,
                 prefix: Annotated[str, Doc("An optional path prefix for the router.")] = "",
                 tags: Annotated[
                     Optional[List[Union[str, Enum]]],
                     Doc(
                         """
                         A list of tags to be applied to all the *path operations* in this
                         router.

                         It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                         """
                     ),
                 ] = None,
                 dependencies: Annotated[
                     Optional[Sequence[params.Depends]],
                     Doc(
                         """
                         A list of dependencies (using `Depends()`) to be applied to all the
                         *path operations* in this router.

                         Read more about it in the
                         [FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                         """
                     ),
                 ] = None,
                 default_response_class: Annotated[
                     Type[Response],
                     Doc(
                         """
                         The default response class to be used.

                         Read more in the
                         [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).
                         """
                     ),
                 ] = Default(JSONResponse),
                 responses: Annotated[
                     Optional[Dict[Union[int, str], Dict[str, Any]]],
                     Doc(
                         """
                         Additional responses to be shown in OpenAPI.

                         It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

                         And in the
                         [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                         """
                     ),
                 ] = None,
                 callbacks: Annotated[
                     Optional[List[BaseRoute]],
                     Doc(
                         """
                         OpenAPI callbacks that should apply to all *path operations* in this
                         router.

                         It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                         """
                     ),
                 ] = None,
                 routes: Annotated[
                     Optional[List[BaseRoute]],
                     Doc(
                         """
                         **Note**: you probably shouldn't use this parameter, it is inherited
                         from Starlette and supported for compatibility.

                         ---

                         A list of routes to serve incoming HTTP and WebSocket requests.
                         """
                     ),
                 ] = None,
                 redirect_slashes: Annotated[
                     bool,
                     Doc(
                         """
                         Whether to detect and redirect slashes in URLs when the client doesn't
                         use the same format.
                         """
                     ),
                 ] = True,
                 default: Annotated[
                     Optional[ASGIApp],
                     Doc(
                         """
                         Default function handler for this router. Used to handle
                         404 Not Found errors.
                         """
                     ),
                 ] = None,
                 dependency_overrides_provider: Annotated[
                     Optional[Any],
                     Doc(
                         """
                         Only used internally by FastAPI to handle dependency overrides.

                         You shouldn't need to use it. It normally points to the `FastAPI` app
                         object.
                         """
                     ),
                 ] = None,
                 on_startup: Annotated[
                     Optional[Sequence[Callable[[], Any]]],
                     Doc(
                         """
                         A list of startup event handler functions.

                         You should instead use the `lifespan` handlers.

                         Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                         """
                     ),
                 ] = None,
                 on_shutdown: Annotated[
                     Optional[Sequence[Callable[[], Any]]],
                     Doc(
                         """
                         A list of shutdown event handler functions.

                         You should instead use the `lifespan` handlers.

                         Read more in the
                         [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                         """
                     ),
                 ] = None,
                 # the generic to Lifespan[AppType] is the type of the top level application
                 # which the router cannot know statically, so we use typing.Any
                 lifespan: Annotated[
                     Optional[Lifespan[Any]],
                     Doc(
                         """
                         A `Lifespan` context manager handler. This replaces `startup` and
                         `shutdown` functions with a single context manager.

                         Read more in the
                         [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                         """
                     ),
                 ] = None,
                 deprecated: Annotated[
                     Optional[bool],
                     Doc(
                         """
                         Mark all *path operations* in this router as deprecated.

                         It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                         """
                     ),
                 ] = None,
                 include_in_schema: Annotated[
                     bool,
                     Doc(
                         """
                         To include (or not) all the *path operations* in this router in the
                         generated OpenAPI.

                         This affects the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                         """
                     ),
                 ] = True,
                 generate_unique_id_function: Annotated[
                     Callable[[APIRoute], str],
                     Doc(
                         """
                         Customize the function used to generate unique IDs for the *path
                         operations* shown in the generated OpenAPI.

                         This is particularly useful when automatically generating clients or
                         SDKs for your API.

                         Read more about it in the
                         [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                         """
                     ),
                 ] = Default(generate_unique_id),
                 ) -> None:
        super().__init__(
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            responses=responses,
            callbacks=callbacks,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=UserDoesntExistAPIRoute,
            default_response_class=default_response_class,
            generate_unique_id_function=generate_unique_id_function,
        )
        self.dependencies.append(Depends(UserDoesntExistGlobalDependency()))


class AuthorizedUserAPIRouter(APIRouter):

    def __init__(self,
                 *,
                 prefix: Annotated[str, Doc("An optional path prefix for the router.")] = "",
                 tags: Annotated[
                     Optional[List[Union[str, Enum]]],
                     Doc(
                         """
                         A list of tags to be applied to all the *path operations* in this
                         router.

                         It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                         """
                     ),
                 ] = None,
                 dependencies: Annotated[
                     Optional[Sequence[params.Depends]],
                     Doc(
                         """
                         A list of dependencies (using `Depends()`) to be applied to all the
                         *path operations* in this router.

                         Read more about it in the
                         [FastAPI docs for Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                         """
                     ),
                 ] = None,
                 default_response_class: Annotated[
                     Type[Response],
                     Doc(
                         """
                         The default response class to be used.

                         Read more in the
                         [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class).
                         """
                     ),
                 ] = Default(JSONResponse),
                 responses: Annotated[
                     Optional[Dict[Union[int, str], Dict[str, Any]]],
                     Doc(
                         """
                         Additional responses to be shown in OpenAPI.

                         It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for Additional Responses in OpenAPI](https://fastapi.tiangolo.com/advanced/additional-responses/).

                         And in the
                         [FastAPI docs for Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies).
                         """
                     ),
                 ] = None,
                 callbacks: Annotated[
                     Optional[List[BaseRoute]],
                     Doc(
                         """
                         OpenAPI callbacks that should apply to all *path operations* in this
                         router.

                         It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
                         """
                     ),
                 ] = None,
                 routes: Annotated[
                     Optional[List[BaseRoute]],
                     Doc(
                         """
                         **Note**: you probably shouldn't use this parameter, it is inherited
                         from Starlette and supported for compatibility.

                         ---

                         A list of routes to serve incoming HTTP and WebSocket requests.
                         """
                     ),
                 ] = None,
                 redirect_slashes: Annotated[
                     bool,
                     Doc(
                         """
                         Whether to detect and redirect slashes in URLs when the client doesn't
                         use the same format.
                         """
                     ),
                 ] = True,
                 default: Annotated[
                     Optional[ASGIApp],
                     Doc(
                         """
                         Default function handler for this router. Used to handle
                         404 Not Found errors.
                         """
                     ),
                 ] = None,
                 dependency_overrides_provider: Annotated[
                     Optional[Any],
                     Doc(
                         """
                         Only used internally by FastAPI to handle dependency overrides.

                         You shouldn't need to use it. It normally points to the `FastAPI` app
                         object.
                         """
                     ),
                 ] = None,
                 on_startup: Annotated[
                     Optional[Sequence[Callable[[], Any]]],
                     Doc(
                         """
                         A list of startup event handler functions.

                         You should instead use the `lifespan` handlers.

                         Read more in the [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                         """
                     ),
                 ] = None,
                 on_shutdown: Annotated[
                     Optional[Sequence[Callable[[], Any]]],
                     Doc(
                         """
                         A list of shutdown event handler functions.

                         You should instead use the `lifespan` handlers.

                         Read more in the
                         [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                         """
                     ),
                 ] = None,
                 # the generic to Lifespan[AppType] is the type of the top level application
                 # which the router cannot know statically, so we use typing.Any
                 lifespan: Annotated[
                     Optional[Lifespan[Any]],
                     Doc(
                         """
                         A `Lifespan` context manager handler. This replaces `startup` and
                         `shutdown` functions with a single context manager.

                         Read more in the
                         [FastAPI docs for `lifespan`](https://fastapi.tiangolo.com/advanced/events/).
                         """
                     ),
                 ] = None,
                 deprecated: Annotated[
                     Optional[bool],
                     Doc(
                         """
                         Mark all *path operations* in this router as deprecated.

                         It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                         """
                     ),
                 ] = None,
                 include_in_schema: Annotated[
                     bool,
                     Doc(
                         """
                         To include (or not) all the *path operations* in this router in the
                         generated OpenAPI.

                         This affects the generated OpenAPI (e.g. visible at `/docs`).

                         Read more about it in the
                         [FastAPI docs for Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#exclude-from-openapi).
                         """
                     ),
                 ] = True,
                 generate_unique_id_function: Annotated[
                     Callable[[APIRoute], str],
                     Doc(
                         """
                         Customize the function used to generate unique IDs for the *path
                         operations* shown in the generated OpenAPI.

                         This is particularly useful when automatically generating clients or
                         SDKs for your API.

                         Read more about it in the
                         [FastAPI docs about how to Generate Clients](https://fastapi.tiangolo.com/advanced/generate-clients/#custom-generate-unique-id-function).
                         """
                     ),
                 ] = Default(generate_unique_id),
                 ) -> None:
        super().__init__(
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            responses=responses,
            callbacks=callbacks,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=UserExistsAPIRoute,
            default_response_class=default_response_class,
            generate_unique_id_function=generate_unique_id_function,
        )
        self.dependencies.append(Depends(UserExistsGlobalDependency()))
