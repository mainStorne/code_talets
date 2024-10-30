from ...dependencies.session import get_session
from ...db.models.roles import Role
from ...schemas.users import RoleCreate, RoleUpdate, RoleRead
from fastapi_sqlalchemy_toolkit import ModelManager
from ...fastapi_crud_toolkit import FastAPICrudToolkit
from ...authentication.users import fastapi_users
from fastapi_sqlalchemy_toolkit import ModelManager
from fastapi_sqlalchemy_toolkit import ordering_depends

manager = ModelManager(Role)

r = FastAPICrudToolkit(
    manager,
    get_session,
    RoleCreate, RoleUpdate, RoleRead,
    fastapi_users.authenticator,
).get_crud_router()
