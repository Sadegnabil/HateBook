from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', post_meta,
    Column('id', Integer),
    Column('username', String(length=20), primary_key=True, nullable=False),
    Column('password', String(length=100)),
    Column('name', String(length=20)),
    Column('surname', String(length=20)),
    Column('birth', String(length=20)),
    Column('registration_date', String(length=20)),
    Column('country', String(length=50)),
)

posts = Table('posts', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('date', VARCHAR(length=20)),
    Column('image_link', VARCHAR(length=100)),
    Column('text', VARCHAR(length=500)),
    Column('hates', INTEGER),
    Column('comments', INTEGER),
    Column('flags', INTEGER),
    Column('author', VARCHAR(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['id'].create()
    pre_meta.tables['posts'].columns['author'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['id'].drop()
    pre_meta.tables['posts'].columns['author'].create()
