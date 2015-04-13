__author__ = 'jmagady'
"""
This is used to downgrade a database by however versions are required
"""

from migrate.versioning import api
from config import  SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

versions = 1  # Number of versions to downgrade
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)  # gets the current db version
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - versions)
"""
migration scripts that are generated contain a downgrade option. api.downgrade runs this option in the migration scripts
"""
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)  # gets the new db version
print('Current database version: ' + str(v))