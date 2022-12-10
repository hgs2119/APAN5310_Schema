"""initialize database

Revision ID: 02b3e5f33765
Revises: 70b196c8934f
Create Date: 2022-12-08 00:04:03.372870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02b3e5f33765'
down_revision = '70b196c8934f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('case_groups', schema=None) as batch_op:
        batch_op.alter_column('group_id',
               existing_type=sa.VARCHAR(length=5),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('commissioners', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('itc_staff', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('product_id',
               existing_type=sa.VARCHAR(length=3),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('product_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=3),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('itc_staff', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('commissioners', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('case_groups', schema=None) as batch_op:
        batch_op.alter_column('group_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=5),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###