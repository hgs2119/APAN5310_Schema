"""initialize database

Revision ID: 70b196c8934f
Revises: ae703a110214
Create Date: 2022-12-08 00:01:19.522983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70b196c8934f'
down_revision = 'ae703a110214'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('date_dim')
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
        batch_op.drop_constraint('commissioners_term_end_date_fkey', type_='foreignkey')
        batch_op.drop_constraint('commissioners_term_begin_date_fkey', type_='foreignkey')

    with op.batch_alter_table('determinations', schema=None) as batch_op:
        batch_op.drop_constraint('determinations_hearing_date_fkey', type_='foreignkey')

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

    with op.batch_alter_table('determinations', schema=None) as batch_op:
        batch_op.create_foreign_key('determinations_hearing_date_fkey', 'date_dim', ['hearing_date'], ['date'])

    with op.batch_alter_table('commissioners', schema=None) as batch_op:
        batch_op.create_foreign_key('commissioners_term_begin_date_fkey', 'date_dim', ['term_begin_date'], ['date'])
        batch_op.create_foreign_key('commissioners_term_end_date_fkey', 'date_dim', ['term_end_date'], ['date'])
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

    op.create_table('date_dim',
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('day', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('daySuffix', sa.VARCHAR(length=2), autoincrement=False, nullable=False),
    sa.Column('weekdayname', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('weekdayname_short', sa.VARCHAR(length=3), autoincrement=False, nullable=False),
    sa.Column('month', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('monthname', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('monthname_short', sa.VARCHAR(length=3), autoincrement=False, nullable=False),
    sa.Column('quarter', sa.SMALLINT(), autoincrement=False, nullable=False),
    sa.Column('quartername', sa.VARCHAR(length=6), autoincrement=False, nullable=False),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('mmyyyy', sa.VARCHAR(length=6), autoincrement=False, nullable=False),
    sa.Column('monthyear', sa.VARCHAR(length=7), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('date', name='date_dim_pkey')
    )
    # ### end Alembic commands ###
