from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "3111990a-e74c-4366-8f1e-77c770304a87"  # TODO

login_manager = LoginManager(app)
login_manager.login_view = "login"

username = 'loiseau'
password = 'loiseau'
host = 'servinfo-maria'
database = 'DBloiseau'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+username+':'+password+'@'+host+'/'+database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
