"""empty message

Revision ID: df4bdf243013
Revises: dfcccf45c6cf
Create Date: 2018-12-27 23:12:54.964178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df4bdf243013'
down_revision = 'dfcccf45c6cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'userplantimage', type_='foreignkey')
    op.drop_column('userplantimage', 'user_plant_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userplantimage', sa.Column('user_plant_id', sa.VARCHAR(length=60), nullable=False))
    op.create_foreign_key(None, 'userplantimage', 'userplant', ['user_plant_id'], ['user_plant_id'])
    # ### end Alembic commands ###