from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', post_meta,
    Column('username', String(length=20), primary_key=True, nullable=False),
    Column('password', String(length=100)),
    Column('name', String(length=20)),
    Column('surname', String(length=20)),
    Column('birth', String(length=20)),
    Column('registration_date', String(length=20)),
    Column('country', String(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['birth'].create()
    post_meta.tables['users'].columns['country'].create()
    post_meta.tables['users'].columns['name'].create()
    post_meta.tables['users'].columns['registration_date'].create()
    post_meta.tables['users'].columns['surname'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['birth'].drop()
    post_meta.tables['users'].columns['country'].drop()
    post_meta.tables['users'].columns['name'].drop()
    post_meta.tables['users'].columns['registration_date'].drop()
    post_meta.tables['users'].columns['surname'].drop()
