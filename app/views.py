"""Toute les routes et les Formulaires"""
from .app import app
from flask import render_template, url_for, redirect, request
from .models import Utilisateur    
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from hashlib import sha256


@app.route("/home/")
def home():
    return render_template("home.html")

class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('Password')
    next = HiddenField()

    def get_authenticated_user(self):
        users = Utilisateur.query.filter(Utilisateur.email==self.email.data).all()
        print(self.email.data)
        #users = Utilisateur.query.get(self.email.data)
        user = None
        for temp_user in users:
            if temp_user.password == self.password.data:
                user = temp_user
        #if user is None:
        #    return None
        return user


@app.route("/", methods=("GET","POST",))
def login():
    print("login")
    f = LoginForm()
    if not f.validate_on_submit():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            #if user.is_prof():
            #    print("prof")
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("connexion.html", form=f)