"""Toute les routes et les Formulaires"""
from .app import app
from flask import render_template, url_for, redirect, request, jsonify
from .models import Utilisateur, Commande, Domaine, Categorie, Materiel, search_commands, commandes_par_domaine, commandes_par_categorie, commandes_par_statut
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

@app.route("/admin/commandes/", methods=("GET", "POST"))
def delivery():
    #initialisation des listes
    liste_commandes = Commande.query.all()
    command = liste_commandes[0]
    liste_domaines = Domaine.query.order_by(Domaine.nom).all()
    liste_categories = Categorie.query.distinct(Categorie.nom).order_by(Categorie.nom).all()
    liste_statuts = []
    for commande in liste_commandes:
        if commande.statut not in liste_statuts:
            liste_statuts.append(commande.statut)

    #tests pour filtrer les résultats
    '''
    text = request.form.get("recherche")
    if text != None and text != "":
        print("test")
        liste_commandes = search_commands(text, liste_commandes)

    domaine = request.form.get("domaine")
    if domaine != None and domaine != "Domaine":
        liste_commandes = commandes_par_domaine(domaine, liste_commandes)

    categorie = request.form.get("categorie")
    if categorie != None and categorie != "Categorie":
        liste_commandes = commandes_par_categorie(categorie, liste_commandes)
    
    statut = request.form.get("statut")
    if statut != None and statut != "Statut":
        liste_commandes = commandes_par_statut(statut, liste_commandes)

    if len(liste_commandes) == 0:
        liste_commandes = None'''
    return render_template("gerer_commandes.html",liste_statuts=liste_statuts, liste_commandes=liste_commandes, liste_domaines=liste_domaines, liste_categories=liste_categories, current_command=command)

@app.route("/get_command_info/<int:numero>,<string:json>", methods=["GET"])
def get_command_info(numero, json):
    command = Commande.query.get(numero)
    if command:
        command_info = {
            'numero': command.numero,
            'nom': command.materiel.nom,
            'domaine': command.materiel.domaine.nom,
            'categorie': command.materiel.categorie.nom,
            'statut': command.statut,
            #'quantite': command.quantite_commandee,
            #'unite': command.materiel.unite,
            'user': command.utilisateur.nom
        }
        if json == "True":
            return jsonify(command_info)
        else:
            return command_info
    else:
        return jsonify({'error': 'Commande non trouvé'}), 404
    
@app.route("/search/<string:value>,<string:id>", methods=["GET"])
def search(value, id):
    value = value[:len(value)-1]
    print(value[:len(value)-1])
    print("test1234"[:2])
    print("test", value=="")
    liste_commandes = Commande.query.all()
    if id == "recherche":
        liste_commandes = search_commands(value, liste_commandes)
    print(len(liste_commandes))
    
    liste_commandes2 = []
    for commande in liste_commandes:
        liste_commandes2.append(get_command_info(commande.numero, False))
    #return render_template("gerer_commandes.html", liste_commandes_search=liste_commandes)
    return jsonify({'liste':liste_commandes2})


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



