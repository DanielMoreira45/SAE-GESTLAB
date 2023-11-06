"""Toute les routes et les Formulaires"""
from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import Utilisateur
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired
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

@app.route('/ajout/util/')
def admin_add():
    f = UtilisateurForm()
    return render_template("ajout-util.html", form=f)

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

@app.route("/ecole/home/")
def ecole_home():
    return render_template("ecole.html")

class UtilisateurForm(FlaskForm):
    idUti = HiddenField('iduti')
    idRole = HiddenField('idrole')
    nomUti = StringField('Nom', validators=[DataRequired()])
    prenomUti = StringField('Prénom', validators=[DataRequired()])
    emailUti = StringField('Email', validators=[DataRequired()])
    mdp = PasswordField('Mot de Passe', validators=[DataRequired()])
    role = SelectField('Rôle', choices=[(1, 'Administrateur'), (2, 'Professeur'), (3, 'Etablissement')])
    modif = RadioField('Droit de Modification', choices=[(True, 'Oui'), (False, 'Non')], validators=[DataRequired()])

@app.route("/save/util/", methods=("POST",))
def save_util():
    f = UtilisateurForm()
    u = Utilisateur(
        id = 1 + db.session.query(db.func.max(Utilisateur.id)).scalar(),
        nom = f.nomUti.data,
        prenom = f.prenomUti.data,
        email = f.emailUti.data,
        password = f.mdp.data,
        id_role = f.role.data
    )
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('admin_add'))
