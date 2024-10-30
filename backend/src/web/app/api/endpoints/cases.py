from ...fastapi_crud_toolkit import FastAPICrudToolkit
from fastapi_sqlalchemy_toolkit import ModelManager
from ...db.models.cases import Case
from ...dependencies.session import get_session
from ...authenticator import Authenticator
from ...schemas.cases import CaseBase, CaseRead, CaseUpdate

m = ModelManager(Case)
auth = Authenticator()

r = FastAPICrudToolkit(m, get_session,
                       CaseRead, CaseUpdate, CaseBase,
                       auth,
                       ).get_crud_router()
