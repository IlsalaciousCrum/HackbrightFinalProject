"""empty message

Revision ID: 395d5c6d6438
Revises: 100f546c7408
Create Date: 2017-01-15 01:32:44.930493

"""

# revision identifiers, used by Alembic.
revision = '395d5c6d6438'
down_revision = '100f546c7408'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    ### end Alembic commands ###