"""Toute les routes et les Formulaires"""
from .app import app, db
from flask import jsonify, render_template, url_for, redirect, request
from .models import Materiel, Utilisateur, Domaine, Categorie, Role
from flask_login import login_required, login_user, logout_user
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
    logout_user()
    return redirect(url_for('login'))

@app.route('/a/')
def admin_add():
    return None #TODO

@app.route('/r/')
def admin_manage():
    return None #TODO

@app.route('/consult/')
@login_required
def consult():
    domaines = Domaine.query.order_by(Domaine.nom).all()
    categories = Categorie.query.order_by(Categorie.nom).all()
    materiels = Materiel.query.order_by(Materiel.nom).all()
    current = materiels[0]
    return render_template("consultation.html", domaines=domaines, categories=categories, materiels=materiels, current_mat=current)

@app.route('/consult/recherche')
def update_materials():
    categories = Categorie.query.order_by(Categorie.nom).all()
    selected_domaine = request.args.get('domaine')
    selected_categorie = request.args.get('categorie')
    search = request.args.get('search')
    liste_materiel = Materiel.query.order_by(Materiel.nom).all()

    if (selected_categorie):        
        liste_materiel = [materiel for materiel in liste_materiel if materiel.code_categorie == int(selected_categorie)]
    
    if (selected_domaine):
        liste_materiel = [materiel for materiel in liste_materiel if materiel.code_domaine == int(selected_domaine)]
       
    if (search):
        liste_materiel = [materiel for materiel in liste_materiel if search.lower() in materiel.nom.lower()]
    
    liste_materiel = [materiel.serialize() for materiel in liste_materiel]
    
    return jsonify({'materiels': liste_materiel})

@app.route('/get_categories')
def get_categories():
    selected_domaine = request.args.get('domaine')
    categories = Categorie.query.order_by(Categorie.nom).all()
    if (selected_domaine):
        categories = [categorie for categorie in categories if categorie.code_domaine == int(selected_domaine)]
    categories = [categorie.serialize() for categorie in categories]
    return jsonify({'categories': categories})

@app.route('/c/')
def delivery():
    return None #TODO

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

@app.route("/get_info_Materiel/<int:reference>", methods=["GET"])
def get_info_Materiel(reference):
    materiel = Materiel.query.get(reference)
    if materiel:
        image_data = materiel.get_image()
        materiel_info = {
            'reference': materiel.reference,
            'nom': materiel.nom,
            'domaine': materiel.domaine.nom,
            'categorie': materiel.categorie.nom,
            'quantite_global': materiel.quantite_globale,
            'quantite_restante': materiel.quantite_restante,
            'complements': materiel.complements,
            'image': image_data
        }
        return jsonify(materiel_info)
    else:
        return jsonify({'error': 'Materiel non trouvé'}), 404
    


