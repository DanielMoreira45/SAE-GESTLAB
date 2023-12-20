"""Toute les routes et les Formulaires"""
from .app import app, db
from .models import Statut, MaterielGenerique, MaterielInstance, Utilisateur, Domaine, Categorie, Role, Commande
from .forms import LoginForm, UtilisateurForm, UserForm, CommandeForm
from flask import jsonify, render_template, url_for, redirect, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from hashlib import sha256
from datetime import datetime
from fpdf import FPDF

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
    liste = Utilisateur.query.order_by(Utilisateur.nomUti).all()
    roles = Role.query.all()
    return render_template("gerer_utilisateurs.html", liste_users=liste, roles=roles, current_user_selected=user)

@app.route("/get_user_info/<int:user_id>", methods=['GET'])
def get_user_info(user_id):
    user = Utilisateur.query.get(user_id)
    role_user = user.get_role()
    if user:
        user_info = {
            'id': user.idUti,
            'nom': user.nomUti,
            'prenom': user.prenomUti,
            'id_role': user.idRole,
            'role_name': role_user.intitule,
            'password': user.mdp,
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
    domaines = Domaine.query.order_by(Domaine.nomD).all()
    categories = Categorie.query.order_by(Categorie.nomC).all()
    materiels = MaterielGenerique.query.order_by(MaterielGenerique.nomMateriel).all()
    current = materiels[0]
    return render_template("consultation.html", domaines=domaines, categories=categories, materiels=materiels, current_mat=current)

@app.route('/consult/recherche')
def update_materials():
    categories = Categorie.query.order_by(Categorie.nomC).all()
    selected_domaine = request.args.get('domaine')
    selected_categorie = request.args.get('categorie')
    search = request.args.get('search')
    liste_materiel = MaterielGenerique.query.order_by(MaterielGenerique.nomMateriel).all()
    if (selected_categorie):        
        liste_materiel = [materiel for materiel in liste_materiel if materiel.code_categorie == int(selected_categorie)]

    if (selected_domaine):
        liste_materiel = [materiel for materiel in liste_materiel if materiel.code_domaine == int(selected_domaine)]

    if (search):
        liste_materiel = [materiel for materiel in liste_materiel if search.lower() in materiel.nom.lower()]
    ####liste_materiel = filtrer(liste_materiel, search, selected_domaine, selected_categorie) ### POUR REFACTORISER LE FILTRAGE

    liste_materiel = [materiel.serialize() for materiel in liste_materiel]
    return jsonify({'materiels': liste_materiel})

@app.route('/get_categories/')
def get_categories():
    selected_domaine = request.args.get('domaine')
    categories = Categorie.query.order_by(Categorie.nomC).all()
    if (selected_domaine):
        categories = [categorie for categorie in categories if categorie.codeD == int(selected_domaine)]
    categories = [categorie.serialize() for categorie in categories]
    return jsonify({'categories': categories})

@app.route('/commandes/creer_pdf/')
def creer_pdf():
    liste_commandes = Commande.query.order_by(Commande.dateCommande).all()
    liste_commandes = filtrer(liste_commandes, request.args.get('search'), request.args.get('domaine'), request.args.get('categorie'), request.args.get('statut'))
    monPdf = FPDF()
    monPdf.add_page()
    monPdf.set_font("Arial", size=30)
    monPdf.cell(0, 10, txt="Commandes", ln=1, align="C")
    monPdf.cell(0, 20, ln=1)
    monPdf.set_font("Arial", size=15)
    monPdf.cell(0, 10, txt="Liste de toutes les commandes : ", ln=1, align="L")
    monPdf.set_font("Arial", size=10)
    for i in range(len(liste_commandes)):
        monPdf.cell(100, 10, txt=" - "+liste_commandes[i].materiel.nomMateriel, ln=i%2, align="L")
    
    monPdf.cell(0, 10, ln=1)

    for commande in liste_commandes:
        monPdf.cell(0, 10, ln=1)
        monPdf.set_font("Arial", size=15)
        monPdf.cell(0, 10, txt=commande.materiel.nomMateriel, ln=1, align="L")
        monPdf.set_font("Arial", size=10)
        monPdf.cell(0, 10, txt="Numéro de commande : "+str(commande.numeroCommande), ln=1, align="L")
        monPdf.cell(0, 10, txt="Statut : "+commande.statut.nomStatut, ln=1, align="L")
        monPdf.cell(0, 10, txt="Domaine : "+commande.materiel.domaine.nomD, ln=1, align="L")
        monPdf.cell(0, 10, txt="Categorie : "+commande.materiel.categorie.nomC, ln=1, align="L")
        monPdf.cell(0, 10, txt="Quantité commandée : "+str(commande.qteCommandee), ln=1, align="L")
        monPdf.cell(0, 10, txt="Commande effectuée par : "+commande.utilisateur.nomUti, ln=1, align="L")

    monPdf.output("commandes.pdf")
    return jsonify({'nom_fichier' : 'commandes.pdf'})


def filtrer(liste, recherche, domaine, categorie, statut=None):
    if (categorie):        
        liste = [commande for commande in liste if commande.materiel.codeC == int(categorie)]

    if (domaine):
        liste = [commande for commande in liste if commande.materiel.codeD == int(domaine)]

    if (recherche):
        liste = [commande for commande in liste if recherche.lower() in commande.materiel.nomMateriel.lower()]

    if (statut):
        liste = [commande for commande in liste if commande.idStatut == int(statut)]

    return liste


@app.route("/commandes/", methods=("GET", "POST"))
def delivery():
    liste_commandes = Commande.query.all()
    liste_domaines = Domaine.query.order_by(Domaine.nomD).all()
    liste_categories = Categorie.query.distinct(Categorie.nomC).order_by(Categorie.nomC).all()
    liste_statuts = Statut.query.distinct(Statut.nomStatut).all()
    return render_template("gerer_commandes.html",liste_statuts=liste_statuts, liste_commandes=liste_commandes, liste_domaines=liste_domaines, liste_categories=liste_categories)

@app.route("/commandes/get_command_info/", methods=["GET"])
def get_command_info():
    numero = request.args.get("id")
    command = Commande.query.get(numero)
    if command:
        command_info = command.serialize()
        return jsonify(command_info)
    else:
        return jsonify({'error': 'Commande non trouvé'}), 404
    
@app.route("/commandes/search/", methods=["GET"])
def search():
    liste_commandes = Commande.query.order_by(Commande.dateCommande).all()
    liste_categories = Categorie.query.all()
    recherche = request.args.get("recherche")
    domaine = request.args.get("domaine")
    categorie = request.args.get("categorie")
    statut = request.args.get("statut")
    
    if (domaine):
        liste_categories = [categorie for categorie in liste_categories if categorie.codeD == int(domaine)]

    
    liste_commandes = filtrer(liste_commandes, recherche, domaine, categorie, statut)    
    liste_commandes = [commande.serialize() for commande in liste_commandes]
    liste_categories = [categorie.serialize() for categorie in liste_categories]

    return jsonify({'liste_commandes':liste_commandes, 'liste_categories':liste_categories})

@app.route("/commandes/validate/")
def validate():
    id = request.args.get("id")[21:]
    commande = Commande.query.get(int(id))
    validee = request.args.get("validee")
    materielGenerique = commande.materiel
    materielGenerique.qteMateriel += commande.qteCommandee
    materielInstance = MaterielInstance(
        idMateriel = db.session.query(db.func.max(MaterielInstance.idMateriel)).scalar()+1,
        qteRestante = commande.qteCommandee,
        datePeremption = '2024-02-02',
        refMateriel = materielGenerique.refMateriel
        )
    db.session.add(materielInstance)
    db.session.commit()
    flash("Commande effectuée avec succès !")
        
    if eval(validee):
        if commande.statut.nomStatut == "En cours":
            commande.statut = Statut.query.filter(Statut.nomStatut == "Livrée").scalar()
        else:
            commande.statut = Statut.query.filter(Statut.nomStatut == "En cours").scalar()
    else:
        commande.statut = Statut.query.filter(Statut.nomStatut == "Non validée").scalar()
    db.session.commit()
    return jsonify({'id':id})

@app.route("/delivery/new/")
@login_required
def new_commande():
    liste_materiel = MaterielGenerique.query.all()
    choix_materiel = [(m.refMateriel, m.nomMateriel) for m in liste_materiel]
    choix_materiel.insert(0, ("", "-- Choisir le matériel --"))
    f = CommandeForm()
    f.materiel_field.choices = choix_materiel
    f.materiel_field.default = ""
    return render_template("new_commande.html", form=f)

@app.route("/delivery/new/save", methods=("POST",))
def save_new_commande():
    f = CommandeForm()
    commande = Commande(
        numeroCommande = 1 + db.session.query(db.func.max(Commande.numeroCommande)).scalar(),
        dateCommande = datetime.utcnow(),
        dateReception = None,
        idStatut = 3,
        qteCommandee = f.quantity_field.data,
        idUti = current_user.idUti,
        refMateriel = f.materiel_field.data
    )
    db.session.add(commande)
    db.session.commit()
    flash("Commande effectuée avec succès !")
    return redirect(url_for('new_commande'))

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
    materiel = MaterielGenerique.query.get(reference)
    if materiel:
        image_data = materiel.get_image()
        materiel_info = {
            'refMateriel': materiel.refMateriel,
            'nomMateriel': materiel.nomMateriel,
            'domaine': materiel.domaine.nomD,
            'categorie': materiel.categorie.nomC,
            'qteMateriel': materiel.qteMateriel,
            'qteMax' : materiel.qteMax,
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
        idUti = 1 + db.session.query(db.func.max(Utilisateur.idUti)).scalar(),
        nomUti = f.nomUti.data,
        prenomUti = f.prenomUti.data,
        emailUti = f.emailUti.data,
        mdp = f.mdp.data,
        idRole = f.role.data,
        modifications = eval(f.modif.data)
    )
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('admin_add'))
