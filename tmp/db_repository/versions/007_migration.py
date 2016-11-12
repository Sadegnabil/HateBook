from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', pre_meta,
    Column('username', VARCHAR(length=20), primary_key=True, nullable=False),
    Column('password', VARCHAR(length=100)),
    Column('name', VARCHAR(length=20)),
    Column('surname', VARCHAR(length=20)),
    Column('birth', VARCHAR(length=20)),
    Column('registration_date', VARCHAR(length=20)),
    Column('country', VARCHAR(length=50)),
    Column('id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['id'].create()
