"""Toute les routes et les Formulaires"""
from .app import app, db
from .models import Materiel, Utilisateur, Domaine, Categorie, Role, Commande , filter_commands

from flask import jsonify, render_template, url_for, redirect, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SelectField, RadioField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from hashlib import sha256
from datetime import datetime
from flask_wtf.file import FileField

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

# Permet la modification de l'utilisateur
class UserForm(FlaskForm):
    id = HiddenField('id')
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    id_role = SelectField('role', validators=[DataRequired()], choices=[(1, 'Administrateur'), (2, 'Professeur'), (3, 'Etablissement')])
    modifications = RadioField('modifications', validators=[DataRequired()])

# Permet l'insertion de l'utilisateur
class UtilisateurForm(FlaskForm):
    idUti = HiddenField('iduti')
    idRole = HiddenField('idrole')
    nomUti = StringField('Nom', validators=[DataRequired()])
    prenomUti = StringField('Prénom', validators=[DataRequired()])
    emailUti = StringField('Email', validators=[DataRequired()])
    mdp = PasswordField('Mot de Passe', validators=[DataRequired()])
    role = SelectField('Rôle', choices=[(1, 'Administrateur'), (2, 'Professeur'), (3, 'Etablissement')])
    modif = RadioField('Droit de Modification', choices=[(True, 'Oui'), (False, 'Non')], validators=[DataRequired()])

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

@app.route('/admin/manage/add/')
@login_required
def admin_add():
    f = UtilisateurForm()
    return render_template("ajout-util.html", form=f)

@app.route("/admin/manage/")
@login_required
def admin_manage(user_id=1):
    user = Utilisateur.query.get(user_id)
    login_user(user)
    liste = Utilisateur.query.order_by(Utilisateur.nom).all()
    roles = Role.query.all()
    return render_template("gerer_utilisateurs.html", liste_users=liste, roles=roles, current_user_selected=user)

@app.route("/get_user_info/<int:user_id>", methods=['GET'])
def get_user_info(user_id):
    user = Utilisateur.query.get(user_id)
    role_user = user.get_role()
    if user:
        user_info = {
            'id': user.id,
            'nom': user.nom,
            'prenom': user.prenom,
            'id_role': user.id_role,
            'role_name': role_user.intitule,
            'password': user.password,
            'modifications': user.modifications
        }
        return jsonify(user_info)
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

@app.route('/update_user/', methods=['POST'])
def update_user():
    les_roles = {'Administrateur': 1, 'Professeur': 2, 'Etablissement': 3}
    f = UserForm()
    user_modified = Utilisateur.query.get(f.id.data)
    user_modified.nom = f.nom.data
    user_modified.prenom = f.prenom.data
    user_modified.password = f.password.data
    if f.id_role.data in les_roles:
        user_modified.id_role = les_roles[f.id_role.data]
    user_modified.modifications = eval(f.modifications.data)
    db.session.commit()
    return redirect(url_for('admin_manage'))

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


@app.route("/ecole/commandes/", methods=("GET", "POST"))
def delivery():
    liste_commandes = Commande.query.all()
    liste_domaines = Domaine.query.order_by(Domaine.nom).all()
    liste_categories = Categorie.query.distinct(Categorie.nom).order_by(Categorie.nom).all()
    liste_statuts = []
    for commande in liste_commandes:
        if commande.statut not in liste_statuts:
            liste_statuts.append(commande.statut)
    return render_template("gerer_commandes.html",liste_statuts=liste_statuts, liste_commandes=liste_commandes, liste_domaines=liste_domaines, liste_categories=liste_categories)

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
            'quantite': command.quantite_commandee,
            'unite': command.materiel.unite,
            'user': command.utilisateur.nom
        }
        if json == "True":
            return jsonify(command_info)
        else:
            return command_info
    else:
        return jsonify({'error': 'Commande non trouvé'}), 404
    
@app.route("/search/<string:recherche>,<string:domaine>,<string:categorie>,<string:statut>", methods=["GET"])
def search(recherche, domaine, categorie, statut):
    liste_commandes = Commande.query.all()
    recherche = recherche[:len(recherche)-1]
    liste_commandes = filter_commands(recherche, domaine, categorie, statut, liste_commandes)

    liste_commandes2 = []
    for commande in liste_commandes:
        liste_commandes2.append(get_command_info(commande.numero, False))
    
    liste_categorie = []
    for categorie in Categorie.query.all():
        if categorie.domaine.nom == domaine or domaine == "Domaine":
            liste_categorie.append(categorie.nom)
    return jsonify({'liste_commandes':liste_commandes2, 'liste_categories':liste_categorie})

@app.route("/validate/<string:validee>,<string:id>")
def validate(validee, id):
    id = id[21:]
    commande = Commande.query.get(id)
    if eval(validee):
        if commande.statut == "En cours":
            commande.statut = "Livrée"
        else:
            commande.statut = "En cours"
    else:
        commande.statut = "Annulée"
    db.session.commit()
    return jsonify({'id':id})


class CommandeForm(FlaskForm):
    materiel_field = SelectField('Matériel', validators=[DataRequired("Merci de sélectionner une option.")])
    quantity_field = IntegerField("Quantité", validators=[DataRequired(), NumberRange(1, 1000)], default=1)

@app.route("/delivery/new/")
@login_required
def new_commande():
    liste_materiel = Materiel.query.all()
    choix_materiel = [(m.reference, m.nom) for m in liste_materiel]
    choix_materiel.insert(0, ("", "-- Choisir le matériel --"))
    f = CommandeForm()
    f.materiel_field.choices = choix_materiel
    f.materiel_field.default = ""
    return render_template("new_commande.html", form=f)

@app.route("/delivery/new/save", methods=("POST",))
def save_new_commande():
    f = CommandeForm()
    commande = Commande(
        numero = 1 + db.session.query(db.func.max(Commande.numero)).scalar(),
        date_commande = datetime.utcnow(),
        date_reception = None,
        statut = "Non validée",
        quantite_commandee = f.quantity_field.data,
        id_util = current_user.id,
        ref_materiel = f.materiel_field.data
    )
    db.session.add(commande)
    db.session.commit()
    flash("Commande effectuée avec succès !")
    return redirect(url_for('new_commande'))

class MaterielForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    photo = FileField('Photo')
    lesD = [(1, 'Appareillage'),
            (2, 'Verrerie et associés'),
            (3, 'Produits Chimiques'),
            (4, 'Matériel de Laboratoire'),
            (5, 'Média'),
            (6, 'Matériel Électrique')]
    lesC = [(1, 'Observation'),
            (2, 'Mesures'),
            (3, 'ExAO'),
            (4, 'Multimédia'),
            (5, 'Expérimentation'),
            (6, 'Divers'),
            (7, 'Verrerie'),
            (8, 'Produits Organiques'),
            (9, 'Produits Minéraux'),
            (10, 'Enzymes'),
            (11, 'Colorants'),
            (12, 'Entretien'),
            (13, 'Autres'),
            (14, 'Appareils de labo'),
            (15, 'Sécurité'),
            (16, 'Fournitures'),
            (17, 'Mobilier'),
            (18, 'Divers'),
            (19, 'Logiciels'),
            (20, 'DVD/VHS'),
            (21, 'Manuels Scolaires'),
            (22, 'Livres Scientifiques'),
            (23, 'Cartes/Posters'),
            (24, 'Divers'),
            (25, 'Générateurs'),
            (26, 'Mesures'),
            (27, 'Récepteurs'),
            (28, 'Connectique'),
            (29, 'Métaux'),
            (30, 'Divers')]

    rangement = StringField('Rangement', validators=[DataRequired()])
    commentaire = TextAreaField('Description' , validators=[DataRequired()])
    quantite = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=0)])
    unite = SelectField('Unité', choices=[None,'cm','g','ml'])
    complements = StringField('Compléments', validators=[DataRequired()])
    ficheFDS = FileField('Fiche De Sécurité')
    seuil_quantite = IntegerField('Seuil de Quantité', validators=[NumberRange(min=0)])
    seuil_peremption = IntegerField('Seuil de Péremption (nb jours)', validators=[NumberRange(min=0)])
    categorie = SelectField('Catégorie', choices=lesC, validators=[DataRequired()])
    domaine = SelectField('Domaine', choices=lesD, validators=[DataRequired()])

@app.route('/materiel/add/')
@login_required
def materiel_add():
    f = MaterielForm()
    return render_template("ajout-materiel.html", form=f)

@app.route("/save/materiel/", methods=("POST",))
def save_materiel():
    f = MaterielForm()
    m = Materiel(
        reference = 1 + db.session.query(db.func.max(Materiel.reference)).scalar(),
        nom = f.nom.data,
        image = f.photo.data,
        fiche_fds = f.ficheFDS.data,
        rangement = f.rangement.data,
        commentaire = f.commentaire.data,
        quantite_globale = f.quantite.data,
        unite = f.unite.data,
        complements = f.complements.data,
        seuil_quantite = f.seuil_quantite.data,
        seuil_peremption = f.seuil_peremption.data,
        code_domaine = f.domaine.data,
        code_categorie = f.categorie.data
    )    
    db.session.add(m)
    db.session.commit()
    return redirect(url_for('consult'))

@app.route("/admin/home/")
@login_required
def admin_home():
    return render_template("admin.html")
  
@app.route("/prof/home/")
@login_required
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
