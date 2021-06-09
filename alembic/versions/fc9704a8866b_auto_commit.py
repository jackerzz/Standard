"""auto commit

Revision ID: fc9704a8866b
Revises: 
Create Date: 2021-06-09 22:13:49.325678

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fc9704a8866b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True, comment='create time of the record'),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True, comment='update time of the record'),
    sa.Column('deleted', sa.Boolean(), nullable=True, comment='delete flag'),
    sa.Column('_groups', sa.String(length=255), nullable=True, comment='user groups'),
    sa.Column('userid', sa.String(length=10), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('hashed_password', sa.String(length=255), nullable=True),
    sa.Column('department', sa.String(length=50), nullable=True),
    sa.Column('role', sa.SmallInteger(), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('last_login', sa.DATETIME(), nullable=True),
    sa.Column('date_joined', sa.DATETIME(), server_default=sa.text('(NOW())'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_userid'), 'user', ['userid'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_userid'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###