from flask import Flask
#from flask_sqlalchemy import SQLAlchemy # SQLALCHEMY FLASK WRAPPER
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # creates an instance of flask named app. not be confused with the app dir
app.config.from_object('config') #tells flask what the name of our config file is/where it is
db = SQLAlchemy(app) #Creates a SQLAlchemy Database object



from app import views, models # the . is used inside the package imports the views.py where our routing is handled. Imports models where our database is described