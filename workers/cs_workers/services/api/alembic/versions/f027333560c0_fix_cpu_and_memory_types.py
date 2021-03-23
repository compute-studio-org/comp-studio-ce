"""Fix cpu and memory types

Revision ID: f027333560c0
Revises: 07a0d0f7e1b4
Create Date: 2021-03-22 14:27:21.523743+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f027333560c0"
down_revision = "07a0d0f7e1b4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "projects",
        "cpu",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=True,
    )
    op.alter_column(
        "projects",
        "memory",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "projects",
        "memory",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )
    op.alter_column(
        "projects",
        "cpu",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
