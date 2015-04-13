# This script is a generic database create script. Creates a blank database
# Imports
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db  # imports the db (Database Object) from our app located in __init__
import os.path


# Create Database begin
db.create_all()  # uses the create_all method on the db object from app/__init__ (Creates a blank db)
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):  # Checks to see if the path at SQLALCHEMY_MIGRATE_REPO exists
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    """
    Creates the directory at SQLALCHEMY_MIGRATE_REPO.This also specifies the repo's name ('database repository')
    also adds a table to the database to track db changes (table default name is migrate_version) 'database repository'
    is the name of the repository. (this is inserted into the table)
    """
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    """
    Marks the db at SQLALCHEMY_DATABASE_URI as under version control at the repo
    located at SQLALCHEMY_MIGRATE_REPO. Inserts a table into the database to track db changes
    (table default name is migrate_version (This can be specified with the api.create)) 'database repository' is the
    name of the repository. (this is inserted into the table)
    """
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
    """
    if the directory already exists at SQLALCHEMY_MIGRATE_REPO, then it will add the database at
    SQLALCHEMY_DATABASE_URI to the repo at SQLALCHEMY_MIGRATE_REPO for version control.
    api.version(SQLALCHEMY_MIGRATE_REPO) gets the latest version in the repo and starts the version control version
    number from this
    """