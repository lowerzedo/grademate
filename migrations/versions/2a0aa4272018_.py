"""empty message

Revision ID: 2a0aa4272018
Revises: 1524cd46271c
Create Date: 2024-05-19 18:20:53.613404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a0aa4272018'
down_revision = '1524cd46271c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_semester', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'semester', ['current_semester'], ['semester_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('current_semester')

    # ### end Alembic commands ###
