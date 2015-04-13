import os

#Web App Configuration File

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]



#Database Config File
database_type = 'sqlite:///'
database_name = 'app.db'
db_migrate_repo = 'db_repository'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = database_type + os.path.join(basedir, database_name)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, db_migrate_repo)