from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, FILE_LOG  # import config.py

app = Flask(__name__)  # creates an instance of flask named app. not be confused with the app dir
app.config.from_object('config')  # tells flask what the name of our config file is/where it is
db = SQLAlchemy(app)  # Creates a SQLAlchemy Database object
lm = LoginManager()  # Create a loginmanager instance
lm.init_app(app)  # initialize with the name of our flask app
lm.login_view = 'login'  # tells flask login manager where our login page is
oid = OpenID(app, os.path.join(basedir, 'tmp'))  # initialize OpenID and tell it where it should store its temp files
from app import views, models  # import from our app views.py and models.py

if not app.debug:  # Checks to see if debug is disabled (False)
    import logging  # import the logging module
    from logging.handlers import SMTPHandler, RotatingFileHandler
    credentials = None  # initialize credentials variable
    if MAIL_USERNAME or MAIL_PASSWORD:  # Checks to see if a username or password is in the config
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)  # If password is present set the credentials variable to a tuple
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'micro blog failure',
                               credentials)  # Setup the SMTP Handler
    file_handler = RotatingFileHandler(FILE_LOG, 'a', 1 * 1024 * 1024, 10)  # Setup file handler
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    """
    sets up the format of the logs that are logged to file
    """
    mail_handler.setLevel(logging.ERROR)  # Set the handler logging level
    file_handler.setLevel(logging.INFO)  # Set the handler logging level
    app.logger.setLevel(logging.INFO)  # set the app logging level to INFO
    app.logger.addHandler(mail_handler)  # add the handler to the logger
    app.logger.addHandler(file_handler)  # add the handler to the logger
    app.logger.info('microblog startup')  # log the startup of the application