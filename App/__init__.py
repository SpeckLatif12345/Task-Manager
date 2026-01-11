"""This file contains initial configuration for the app"""

from flask import Flask
from flask_wtf import CSRFProtect
from sql_alchemy_initialize import db
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect()  # Protects  app from CSRF attacks (Cross-Site Request Forgery)
csrf.init_app(app)


# passing app instance to db
db.init_app(app)

""" these are imported last , because they depend on app variable ,  flask needs 
 needs to be configured first because they depend on flask , if we try to import 
  them before app  then we will get circular-import errors """
from App import routes, models
