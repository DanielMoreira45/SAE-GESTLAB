from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os.path

app = Flask(__name__)
user = 'root'
password = 'root'
host = 'localhost'
port = '3306'
database = 'dbmoreira'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://'+user+':'+password+'@'+host+':'+port+'/'+database
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = "3111990a-e74c-4366-8f1e-77c770304a87"  # TODO

login_manager = LoginManager(app)
login_manager.login_view = "login"
