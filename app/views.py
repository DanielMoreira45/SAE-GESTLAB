"""Toute les routes et les Formulaires"""
from .app import app
from flask import render_template, url_for, redirect, request
from .models import Utilisateur    
from flask_login import login_user, user_logged_in, user_login_confirmed, confirm_login
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from hashlib import sha256

class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    password_incorrect = ""
    next = HiddenField()

    def get_authenticated_user(self):
        users = Utilisateur.query.filter(Utilisateur.email==self.email.data).all()
        user = None
        for temp_user in users:
            if temp_user.password == self.password.data:
                user = temp_user
        return user
    
    def has_content(self):
        return self.password.data != "" or self.email.data != ""
    
    def show_password_incorrect(self):
        self.password_incorrect = "Email ou mot de passe incorrect"

@app.route("/login/", methods=("GET","POST",))
def login():
    f = LoginForm()

    if request.method == "POST":
        if request.form["submit_button"] == "mdp":
            return render_template("bug.html")
    if f.is_submitted():
        if f.has_content():
            f.show_password_incorrect()
    if not f.validate_on_submit():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            if user.is_prof():
                next = f.next.data or url_for("prof_home")
            elif user.is_admin():
                next = f.next.data or url_for("admin_home")
            elif user.is_etablissement():
                next = f.next.data or url_for("ecole_home")
            return redirect(next)

    return render_template("connexion.html", form=f)



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

@app.route("/prof/home/")
def prof_home():
    return render_template("prof.html")

@app.route("/admin/home/")
def admin_home():
    return render_template("admin.html")

@app.route("/ecole/home/", methods=("GET","POST",))
def ecole_home():
    print()
    return render_template("ecole.html", prenom=user_logged_in)
