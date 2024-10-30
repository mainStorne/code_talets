"""empty message

Revision ID: 077112e32df3
Revises: 446c1283e739
Create Date: 2024-10-30 17:00:49.557132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy

from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from app.db.models.users import User
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory


class Factory(SQLAlchemyFactory):
    __is_base_factory__ = True
    __set_relationships__ = False


# revision identifiers, used by Alembic.
revision: str = '077112e32df3'
down_revision: Union[str, None] = '446c1283e739'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('specialities',
                    sa.Column('name', sa.String(length=300), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('urls', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('questions',
                    sa.Column('name', sa.String(length=300), nullable=False),
                    sa.Column('speciality_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['speciality_id'], ['specialities.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    # ### end Alembic commands ###
    async def seed_db(connection: AsyncConnection):
        session = AsyncSession(bind=connection)
        Factory.__async_session__ = session
        u_factory = Factory.create_factory(User)
        seeds = [{1: 'Работать над созданием приложений с виртуальной или дополненной реальностью',
                  2: 'Делать красивые и аккуратные сайты из дизайн-макетов',
                  3: 'Делать важную, но малозаметную работу: оптимизировать, настраивать и обеспечивать надёжность сайта',
                  4: 'Искать ошибки и придумывать способы, как лучше их исправить'},
                 {1: 'Создавать плавные переходы и интересные анимации в мобильном приложении',
                  2: 'Придумывать новые и нетривиальные способы поиска ошибок',
                  3: 'Программировать сайты так, чтобы на любых устройствах они отображались корректно',
                  4: 'Разносторонне продумывать логику и внутреннюю структуру будущей программы'},
                 {1: 'Делать мобильное приложение удобным и понятным для пользователя',
                  2: 'Делать сайты удобными и понятными для пользователей',
                  3: 'Быть специалистом, от внимания которого не ускользнёт ни один сдвинутый пиксель',
                  4: 'Уметь делать всю работу целиком,от идеи и до последней строчки кода'},
                 {1: 'Активно использовать в программировании микрофон, камеру, геолокацию и другие функции',
                  2: 'Придумывать программы, которые автоматически ищут ошибки',
                  3: 'Уметь одинаково хорошо настраивать операционные системы и разрабатывать сайты',
                  4: 'Делать сайты удобными для людей с ограниченными возможностями'},
                 {1: 'Работать над программированием новых фишек мобильного приложения',
                  2: 'Создавать интересные эффектыи анимации на сайте ',
                  3: 'Разбираться во всех областях программирования, пусть даже и поверхностно',
                  4: 'Педантично, шаг за шагом, проверять правильность работы каждой детали'}]

        # await u_factory.create_async(id=695473622, is_superuser=True)

    op.run_async(seed_db)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questions')
    op.drop_table('specialities')
    # ### end Alembic commands ###
