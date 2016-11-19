from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=20)),
    Column('surname', String(length=20)),
    Column('username', String(length=20)),
    Column('password', String(length=100)),
    Column('mood', String(length=100), default=ColumnDefault('Hello world!')),
    Column('birth', String(length=20)),
    Column('registration_date', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['mood'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['mood'].drop()
