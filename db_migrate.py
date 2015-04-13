__author__ = 'jmagady'
'''
This script records database migrations so that changes made during the development lifecycle can be applied
to the production database easily
'''

import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
'''
Gets the current version of the database from the repo and stores it in variable 'v'
'''
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/{version}_migration.py'.format(version='{:03}'.format(v+1)))
'''
This creates the string that wil be used to create the file where the migration script will be stored. it will be
formatted XXX_migration.py where XXX is version number
'''
tmp_module = imp.new_module('old_model')  # Creates a new blank module named 'old_model' stored in tmp_module
old_module = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
'''
dumps the current database as a python model and stores it in old_module
'''
exec(old_module, tmp_module.__dict__)
'''
takes the python code stored in old_module and turns it into a python object stored in tmp_module. arg 2 of exec
is required to be a dict
'''
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta, db.metadata)
'''
Creates a script object that will upgrade your database to the current one by comparing the current database to the
currently defined database models in your program
'''
open(migration, 'wt').write(script)  # Opens a file at migration and writes the script object
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
'''
runs the migration script to upgrade/migrate to the latest version of your defined database
'''
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)  # gets the current version of your database
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))