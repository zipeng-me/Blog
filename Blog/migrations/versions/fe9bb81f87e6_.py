"""empty message

Revision ID: fe9bb81f87e6
Revises: 7d224b223b2c
Create Date: 2019-01-24 12:31:56.122031

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fe9bb81f87e6'
down_revision = '7d224b223b2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table_comment(
        'blogtype',
        existing_comment='???? - ????,????,????',
        schema=None
    )
    op.drop_table_comment(
        'category',
        existing_comment='????',
        schema=None
    )
    op.alter_column('reply', 'topic_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('reply', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_table_comment(
        'reply',
        existing_comment='????',
        schema=None
    )
    op.drop_table_comment(
        'topic',
        existing_comment='????',
        schema=None
    )
    op.drop_table_comment(
        'user',
        existing_comment='?????',
        schema=None
    )
    op.alter_column('voke', 'topic_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('voke', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_table_comment(
        'voke',
        existing_comment='??',
        schema=None
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table_comment(
        'voke',
        '??',
        existing_comment=None,
        schema=None
    )
    op.alter_column('voke', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('voke', 'topic_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.create_table_comment(
        'user',
        '?????',
        existing_comment=None,
        schema=None
    )
    op.create_table_comment(
        'topic',
        '????',
        existing_comment=None,
        schema=None
    )
    op.create_table_comment(
        'reply',
        '????',
        existing_comment=None,
        schema=None
    )
    op.alter_column('reply', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('reply', 'topic_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.create_table_comment(
        'category',
        '????',
        existing_comment=None,
        schema=None
    )
    op.create_table_comment(
        'blogtype',
        '???? - ????,????,????',
        existing_comment=None,
        schema=None
    )
    # ### end Alembic commands ###
