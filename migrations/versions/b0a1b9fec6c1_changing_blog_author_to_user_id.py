"""changing blog author to user_id

Revision ID: b0a1b9fec6c1
Revises: 5d53bc9adb48
Create Date: 2022-05-18 11:48:43.924796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0a1b9fec6c1'
down_revision = '5d53bc9adb48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogs', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('blogs_blogAuthor_fkey', 'blogs', type_='foreignkey')
    op.create_foreign_key(None, 'blogs', 'users', ['user_id'], ['id'])
    op.drop_column('blogs', 'blogAuthor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogs', sa.Column('blogAuthor', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'blogs', type_='foreignkey')
    op.create_foreign_key('blogs_blogAuthor_fkey', 'blogs', 'users', ['blogAuthor'], ['id'])
    op.drop_column('blogs', 'user_id')
    # ### end Alembic commands ###
