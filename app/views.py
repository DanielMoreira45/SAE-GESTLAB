"""Toute les routes et les Formulaires"""
from .app import app, db
from .models import AlerteQuantite, Statut, MaterielGenerique, MaterielInstance, Utilisateur, Domaine, Categorie, Role, Commande, filter_commands
from .forms import LoginForm, UtilisateurForm, UserForm, CommandeForm, MaterielForm, MaterielModificationForm

from flask import jsonify, render_template, url_for, redirect, request, flash
from flask_login import login_required, login_user, logout_user, current_user
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
    f = MaterielModificationForm(materiel=current)
    
    f.set_domaine_choices([(domaine.codeD, domaine.nomD) for domaine in domaines])
    f.set_categorie_choices([(categorie.codeC, categorie.nomC) for categorie in categories if categorie.codeD == current.codeD])
    # f.set_categorie_choices([(categorie.codeC, categorie.nomC) for categorie in categories])
    return render_template("consultation.html",form = f ,domaines=domaines, categories=categories, materiels=materiels, current_mat=current)

@app.route('/consult/recherche')
def update_materials():
    categories = Categorie.query.order_by(Categorie.nomC).all()
    selected_domaine = request.args.get('domaine')
    selected_categorie = request.args.get('categorie')
    search = request.args.get('search')
    liste_materiel = MaterielGenerique.query.order_by(MaterielGenerique.nomMateriel).all()
    if (selected_categorie):        
        liste_materiel = [materiel for materiel in liste_materiel if materiel.codeC == int(selected_categorie)]

    if (selected_domaine):
        liste_materiel = [materiel for materiel in liste_materiel if materiel.codeD == int(selected_domaine)]

    if (search):
        liste_materiel = [materiel for materiel in liste_materiel if search.lower() in materiel.nomMateriel.lower()]

    liste_materiel = [materiel.serialize() for materiel in liste_materiel]
    return jsonify({'materiels': liste_materiel})

@app.route('/consult/enregistrer', methods=['POST'])
def save_material():
    materiel = MaterielGenerique.query.get(request.form["hiddenref"])
    if materiel:
        materiel.nom = request.form["nom"]
        materiel.reference = request.form["reference"]
        materiel.quantite_max = request.form["quantiteMax"]
        materiel.quantite_globale = request.form["quantiteTot"]
        # materiel.quantite_restante = request.form["quantiteRes"]
        materiel.complements = request.form["description"]
        #Changer le domaine et la catégorie
        materiel.codeD = request.form["domaine"]
        materiel.codeC = request.form["categorie"]

        db.session.commit()
        return redirect(url_for('consult'))
    return redirect(url_for('consult'))

@app.route('/consult/supprimer/<int:id>')
def delete_material(id):
    materiel = MaterielGenerique.query.get(id)
    alertes = AlerteQuantite.query.filter_by(refMateriel=id).all()
    if materiel:
        for alerte in alertes:
            db.session.delete(alerte)
        db.session.delete(materiel)
        db.session.commit()
        response = {'status': 'success'}
    else:
        response = {'status': 'error'}
    return jsonify(response)

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
    liste_commandes = filtrer_commandes(request.args.get('search'), request.args.get('domaine'), request.args.get('categorie'), request.args.get('statut'))
    monPdf = FPDF()
    monPdf.add_page()
    monPdf.set_font("Arial", size=30)
    monPdf.cell(0, 10, txt="Commandes", ln=1, align="C")
    monPdf.cell(0, 20, ln=1)
    monPdf.set_font("Arial", size=15)
    monPdf.cell(0, 10, txt="Liste de toutes les commandes : ", ln=1, align="L")
    monPdf.set_font("Arial", size=10)
    for i in range(len(liste_commandes)):
            monPdf.cell(100, 10, txt=" - "+liste_commandes[i].materiel.nom, ln=i%2, align="L")
    
    monPdf.cell(0, 10, ln=1)

    for commande in liste_commandes:
        monPdf.cell(0, 10, ln=1)
        monPdf.set_font("Arial", size=15)
        monPdf.cell(0, 10, txt=commande.materiel.nom, ln=1, align="L")
        monPdf.set_font("Arial", size=10)
        monPdf.cell(0, 10, txt="Numéro de commande : "+str(commande.numero), ln=1, align="L")
        monPdf.cell(0, 10, txt="Statut : "+commande.statut, ln=1, align="L")
        monPdf.cell(0, 10, txt="Domaine : "+commande.materiel.domaine.nom, ln=1, align="L")
        monPdf.cell(0, 10, txt="Categorie : "+commande.materiel.categorie.nom, ln=1, align="L")
        monPdf.cell(0, 10, txt="Quantité commandée : "+str(commande.quantite_commandee), ln=1, align="L")
        monPdf.cell(0, 10, txt="Commande effectuée par : "+commande.utilisateur.nom, ln=1, align="L")

    monPdf.output("commandes.pdf")
    return jsonify({'nom_fichier' : 'commandes.pdf'})


def filtrer_commandes(recherche, domaine, categorie, statut):
    liste_commandes = Commande.query.order_by(Commande.date_commande).all()
    if (categorie!="Categorie"):        
        liste_commandes = [commande for commande in liste_commandes if commande.materiel.categorie.nom == categorie]

    if (domaine!="Domaine"):
        liste_commandes = [commande for commande in liste_commandes if commande.materiel.domaine.nom == domaine]

    if (recherche):
        liste_commandes = [commande for commande in liste_commandes if recherche.lower() in commande.materiel.nom.lower()]

    if (statut!="Statut"):
        liste_commandes = [commande for commande in liste_commandes if commande.statut == statut]

    return liste_commandes


@app.route("/commandes/", methods=("GET", "POST"))
def delivery():
    liste_commandes = Commande.query.all()
    liste_domaines = Domaine.query.order_by(Domaine.nomD).all()
    liste_categories = Categorie.query.distinct(Categorie.nomC).order_by(Categorie.nomC).all()
    liste_statuts = []
    for commande in liste_commandes:
        if commande.statut.nomStatut not in liste_statuts:
            liste_statuts.append(commande.statut)
    return render_template("gerer_commandes.html",liste_statuts=liste_statuts, liste_commandes=liste_commandes, liste_domaines=liste_domaines, liste_categories=liste_categories)

@app.route("/commandes/get_command_info/", methods=["GET"])
def get_command_info():
    numero = request.args.get("id")
    command = Commande.query.get(numero)
    statut = Statut.query.get(command.idStatut)
    if command:
        command_info = command.serialize()
        json = request.args.get("json")
        if json == "True":
            return jsonify(command_info)
        else:
            return command_info
    else:
        return jsonify({'error': 'Commande non trouvé'}), 404
    
@app.route("/commandes/search/", methods=["GET"])
def search():
    liste_commandes = Commande.query.all()
    liste_categories = Categorie.query.all()
    print(liste_categories)
    recherche = request.args.get("recherche")
    recherche = recherche[:len(recherche)]
    domaine = request.args.get("domaine")
    categorie = request.args.get("categorie")
    print(categorie)
    statut = request.args.get("statut")

    if (domaine):
        liste_commandes = [commande for commande in liste_commandes if commande.materiel.code_domaine == int(domaine)]
        liste_categories = [categorie for categorie in liste_categories if categorie.code_domaine == int(domaine)]

    if (categorie):        
        liste_commandes = [commande for commande in liste_commandes if commande.materiel.code_categorie == int(categorie)]

    if (statut):
        liste_commandes = [commande for commande in liste_commandes if commande.statut == statut]

    if (recherche):
        liste_commandes = [commande for commande in liste_commandes if recherche.lower() in commande.materiel.nom.lower()]
    
    liste_commandes = [commande.serialize() for commande in liste_commandes]
    liste_categories = [categorie.serialize() for categorie in liste_categories]

    return jsonify({'liste_commandes':liste_commandes, 'liste_categories':liste_categories})

@app.route("/commandes/validate/")
def validate():
    id = request.args.get("id")
    id = id[21:]
    commande = Commande.query.get(id)
    validee = request.args.get("validee")
    if eval(validee):
        if commande.statut == "En cours":
            commande.statut = "Livrée"
        else:
            commande.statut = "En cours"
    else:
        commande.statut = "Annulée"
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

@app.route('/materiel/add/')
@login_required
def materiel_add():
    f = MaterielForm()
    return render_template("ajout-materiel.html", form=f)

@app.route("/save/materiel/", methods=("POST",))
def save_materiel():
    f = MaterielForm()
    m = MaterielGenerique(
        reference = 1 + db.session.query(db.func.max(MaterielGenerique.reference)).scalar(),
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
    materiel = MaterielGenerique.query.get(reference)
    if materiel:
        liste_categories = Categorie.query.filter_by(codeD=materiel.codeD).all()
        liste_categories = [categorie.serialize() for categorie in liste_categories]
        image_data = materiel.get_image()
        materiel_info = {
            'reference': materiel.refMateriel,
            'nom': materiel.nomMateriel,
            'domaine': materiel.domaine.codeD,
            'categorie': materiel.categorie.codeC,
            'quantite_max': materiel.qteMax,
            'quantite_global': materiel.qteMateriel,
            # 'quantite_restante': materiel.quantite_restante,
            'complements': materiel.complements,
            'image': image_data,
            'categories': liste_categories
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
