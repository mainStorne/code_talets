"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy
${imports if imports else ""}
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from app.db.models.users import User
from app.db.models.roles import Role
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

class Factory(SQLAlchemyFactory):
    __is_base_factory__ = True
    __set_relationships__ = True

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}
    async def seed_db(connection: AsyncConnection):
        session = AsyncSession(bind=connection)
        Factory.__async_session__ = session
        u_factory = Factory.create_factory(User)
        roles = ['driver', 'manager', 'admin']
        for role in roles:
            role_in_db = Role(name=role)
            session.add(role_in_db)
            await session.commit()
            for i in range(10):
                await u_factory.create_async(id=role_in_db.id)

    op.run_async(seed_db)


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
