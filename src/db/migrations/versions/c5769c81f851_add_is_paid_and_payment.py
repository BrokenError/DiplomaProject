"""add is_paid and payment

Revision ID: c5769c81f851
Revises: a0f2b16a57e2
Create Date: 2024-05-07 18:22:54.822245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5769c81f851'
down_revision = 'a0f2b16a57e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('payment_method', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('is_paid', sa.Boolean(), nullable=False))
    op.drop_column('orders', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('orders', 'is_paid')
    op.drop_column('orders', 'payment_method')
    # ### end Alembic commands ###
