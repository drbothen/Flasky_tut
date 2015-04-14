from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir  # import config.py

app = Flask(__name__)  # creates an instance of flask named app. not be confused with the app dir
app.config.from_object('config')  # tells flask what the name of our config file is/where it is
db = SQLAlchemy(app)  # Creates a SQLAlchemy Database object
lm = LoginManager()  # Create a loginmanager instance
lm.init_app(app)  # initialize with the name of our flask app
lm.login_view = 'login'  # tells flask login manager where our login page is
oid = OpenID(app, os.path.join(basedir, 'tmp'))  # initialize OpenID and tell it where it should store its temp files
from app import views, models  # import from our app views.py and models.py