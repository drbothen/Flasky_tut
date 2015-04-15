"""
This file is the main configuration file for the application. This will set all the static configurations
"""

import os

# Web App Configuration File

WTF_CSRF_ENABLED = True  # Enables cross site scripting protection
SECRET_KEY = 'you-will-never-guess'  # This is required when CSRF is enabled (Should be changed to a more secure key)

OPENID_PROVIDERS = [  # defines a list of dicts (array) of openid providers
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

# Database Config File
database_type = 'sqlite:///'
database_name = 'app.db'
db_migrate_repo = 'db_repository'

basedir = os.path.abspath(os.path.dirname(__file__))  # defines that base directory (Where the file is located)

SQLALCHEMY_DATABASE_URI = database_type + os.path.join(basedir, database_name)  # sets the SQL uri for SQLAlchemy
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, db_migrate_repo)  # Sets the location of the migrate repo

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrators list
ADMINS = ['you@example.com']


