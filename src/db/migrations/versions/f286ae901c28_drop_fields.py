"""drop fields

Revision ID: f286ae901c28
Revises: cd5f7e9bc0df
Create Date: 2024-05-28 17:55:31.229484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f286ae901c28'
down_revision = 'cd5f7e9bc0df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('accessories_id_product_fkey', 'accessories', type_='foreignkey')
    op.create_foreign_key(None, 'accessories', 'products', ['id_product'], ['id'], ondelete='CASCADE')
    op.drop_constraint('favourites_id_user_fkey', 'favourites', type_='foreignkey')
    op.drop_constraint('favourites_id_product_fkey', 'favourites', type_='foreignkey')
    op.create_foreign_key(None, 'favourites', 'users', ['id_user'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'favourites', 'products', ['id_product'], ['id'], ondelete='CASCADE')
    op.drop_constraint('laptops_id_product_fkey', 'laptops', type_='foreignkey')
    op.create_foreign_key(None, 'laptops', 'products', ['id_product'], ['id'], ondelete='CASCADE')
    op.drop_column('laptops', 'processor_frequency')
    op.drop_column('laptops', 'screen_diagonal')
    op.drop_constraint('order_items_id_user_fkey', 'order_items', type_='foreignkey')
    op.drop_constraint('order_items_id_product_fkey', 'order_items', type_='foreignkey')
    op.drop_constraint('order_items_id_order_fkey', 'order_items', type_='foreignkey')
    op.create_foreign_key(None, 'order_items', 'orders', ['id_order'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'order_items', 'users', ['id_user'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'order_items', 'products', ['id_product'], ['id'], ondelete='CASCADE')
    op.drop_constraint('orders_id_user_fkey', 'orders', type_='foreignkey')
    op.create_foreign_key(None, 'orders', 'users', ['id_user'], ['id'], ondelete='SET NULL')
    op.drop_constraint('reviews_id_user_fkey', 'reviews', type_='foreignkey')
    op.drop_constraint('reviews_id_product_fkey', 'reviews', type_='foreignkey')
    op.create_foreign_key(None, 'reviews', 'users', ['id_user'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'reviews', 'products', ['id_product'], ['id'], ondelete='CASCADE')
    op.drop_constraint('smartphones_id_product_fkey', 'smartphones', type_='foreignkey')
    op.create_foreign_key(None, 'smartphones', 'products', ['id_product'], ['id'], ondelete='CASCADE')
    op.drop_column('smartphones', 'processor_frequency')
    op.drop_column('smartphones', 'screen_diagonal')
    op.drop_constraint('smartwatches_id_product_fkey', 'smartwatches', type_='foreignkey')
    op.create_foreign_key(None, 'smartwatches', 'products', ['id_product'], ['id'], ondelete='CASCADE')
    op.drop_column('smartwatches', 'screen_diagonal')
    op.drop_constraint('tablets_id_product_fkey', 'tablets', type_='foreignkey')
    op.create_foreign_key(None, 'tablets', 'products', ['id_product'], ['id'], ondelete='CASCADE')
    op.drop_column('tablets', 'processor_frequency')
    op.drop_column('tablets', 'screen_diagonal')
    op.drop_constraint('televisions_id_product_fkey', 'televisions', type_='foreignkey')
    op.create_foreign_key(None, 'televisions', 'products', ['id_product'], ['id'], ondelete='CASCADE')
    op.drop_column('televisions', 'screen_diagonal')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('televisions', sa.Column('screen_diagonal', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'televisions', type_='foreignkey')
    op.create_foreign_key('televisions_id_product_fkey', 'televisions', 'products', ['id_product'], ['id'])
    op.add_column('tablets', sa.Column('screen_diagonal', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('tablets', sa.Column('processor_frequency', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'tablets', type_='foreignkey')
    op.create_foreign_key('tablets_id_product_fkey', 'tablets', 'products', ['id_product'], ['id'])
    op.add_column('smartwatches', sa.Column('screen_diagonal', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'smartwatches', type_='foreignkey')
    op.create_foreign_key('smartwatches_id_product_fkey', 'smartwatches', 'products', ['id_product'], ['id'])
    op.add_column('smartphones', sa.Column('screen_diagonal', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('smartphones', sa.Column('processor_frequency', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'smartphones', type_='foreignkey')
    op.create_foreign_key('smartphones_id_product_fkey', 'smartphones', 'products', ['id_product'], ['id'])
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.create_foreign_key('reviews_id_product_fkey', 'reviews', 'products', ['id_product'], ['id'])
    op.create_foreign_key('reviews_id_user_fkey', 'reviews', 'users', ['id_user'], ['id'])
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.create_foreign_key('orders_id_user_fkey', 'orders', 'users', ['id_user'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.create_foreign_key('order_items_id_order_fkey', 'order_items', 'orders', ['id_order'], ['id'])
    op.create_foreign_key('order_items_id_product_fkey', 'order_items', 'products', ['id_product'], ['id'])
    op.create_foreign_key('order_items_id_user_fkey', 'order_items', 'users', ['id_user'], ['id'])
    op.add_column('laptops', sa.Column('screen_diagonal', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('laptops', sa.Column('processor_frequency', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'laptops', type_='foreignkey')
    op.create_foreign_key('laptops_id_product_fkey', 'laptops', 'products', ['id_product'], ['id'])
    op.drop_constraint(None, 'favourites', type_='foreignkey')
    op.drop_constraint(None, 'favourites', type_='foreignkey')
    op.create_foreign_key('favourites_id_product_fkey', 'favourites', 'products', ['id_product'], ['id'])
    op.create_foreign_key('favourites_id_user_fkey', 'favourites', 'users', ['id_user'], ['id'])
    op.drop_constraint(None, 'accessories', type_='foreignkey')
    op.create_foreign_key('accessories_id_product_fkey', 'accessories', 'products', ['id_product'], ['id'])
    # ### end Alembic commands ###