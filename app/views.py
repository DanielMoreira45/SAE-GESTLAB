"""Toute les routes et les Formulaires"""

from flask import render_template
from flask_login import login_user

from .app import app
from .models import Utilisateur


@app.route('/test/')
def test():
    user = Utilisateur.query.get(2)
    login_user(user)
    return render_template('test.html')

@app.route('/login/')
def login():
    return None #TODO

@app.route('/logout/')
def logout():
    return None #TODO

@app.route('/a/')
def admin_add():
    return None #TODO

@app.route('/r/')
def admin_manage():
    return None #TODO

@app.route('/b/')
def consult():
    return None #TODO

@app.route('/c/')
def delivery():
    return None #TODO

@app.route('/d/')
def new_commande():
    return None #TODO
