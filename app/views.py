"""Toute les routes et les Formulaires"""
from .app import app
from flask import render_template, url_for, redirect, request
from .models import Utilisateur, Commande, Domaine, Categorie, search_commands
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from hashlib import sha256

class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    password_incorrect = ""
    next = HiddenField()

    def get_authenticated_user(self):
        user = Utilisateur.query.filter_by(email=self.email.data).first()
        if user and user.password == self.password.data:
            return user
    
    def has_content(self):
        return self.password.data != "" or self.email.data != ""
    
    def show_password_incorrect(self):
        self.password_incorrect = "Email ou mot de passe incorrect"

@app.route("/")
def home():
    return render_template("home.html")

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
    logout_user()
    return redirect(url_for('login'))

@app.route('/a/')
def admin_add():
    return None #TODO

@app.route('/r/')
def admin_manage():
    return None #TODO

@app.route('/b/')
def consult():
    return None #TODO

@app.route("/admin/commandes/<numero>", methods=("GET", "POST"))
def delivery(numero=0):
    liste_commandes = Commande.query.all()
    command = liste_commandes[int(numero)-1]
    liste_domaines = Domaine.query.all()
    liste_categories = Categorie.query.all()
    text = request.form.get("recherche")
    if text != None and text != "":
        liste_commandes = search_commands(text)

    return render_template("gerer_commandes.html", liste_commandes=liste_commandes, current_command=command, liste_domaines=liste_domaines, liste_categories=liste_categories)

@app.route('/d/')
def new_commande():
    return None #TODO

@app.route("/admin/home/")
@login_required
def admin_home():
    return render_template("admin.html")
  
@app.route("/prof/home/")
def prof_home():
    return render_template("prof.html")

@app.route("/ecole/home/", methods=("GET","POST",))
@login_required
def ecole_home():
    return render_template("ecole.html")

