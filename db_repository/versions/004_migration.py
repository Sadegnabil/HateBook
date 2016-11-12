from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author', String(length=20)),
    Column('date', String(length=20)),
    Column('image_link', String(length=100)),
    Column('text', String(length=500)),
    Column('hates', Integer),
    Column('comments', Integer),
    Column('flags', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['posts'].columns['author'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['posts'].columns['author'].drop()
