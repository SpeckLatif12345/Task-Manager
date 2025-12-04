""" This file contains initial configuration for the app """

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sql_alchemy_initialize import db
from config import Config



app=Flask(__name__)
app.config.from_object(Config)

# passing app instance to db
db.init_app(app)

""" these are imported last , because they depend on app variable ,  flask needs 
 needs to be configured first because they depend on flask , if we try to import 
  them before app  then we will get circular-import errors """
from App import routes,models


