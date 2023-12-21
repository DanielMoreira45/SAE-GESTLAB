"""Toute les routes et les Formulaires"""
import os
from .app import app, db
from .models import AlerteQuantite, Statut, MaterielGenerique, MaterielInstance, Utilisateur, Domaine, Categorie, Role, Commande, getToutesLesAlertes
from .forms import LoginForm, UtilisateurForm, UserForm, CommandeForm, MaterielForm, MaterielModificationForm, MaterielInstanceForm

from flask import jsonify, render_template, send_from_directory, url_for, redirect, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
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
    return render_template("connexion.html", form=f, alertes=getToutesLesAlertes())

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/manage/add/')
@login_required
def admin_add():
    f = UtilisateurForm()
    return render_template("ajout-util.html", form=f, alertes=getToutesLesAlertes())

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
    
@app.route("/get_last_user_info/", methods=['GET'])
def get_last_user_info():
    user = Utilisateur.query.get(db.session.query(db.func.max(Utilisateur.idUti)).scalar())
    print(db.session.query(db.func.max(Utilisateur.idUti)).scalar())
    if user:
        user_info = {
            'email': user.emailUti,
            'password': user.mdp
        }
        print(user_info)
        print(jsonify(user_info))
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
    f = MaterielModificationForm(materielG=current)
    f.set_domaine_choices([(domaine.codeD, domaine.nomD) for domaine in domaines])
    f.set_categorie_choices([(categorie.codeC, categorie.nomC) for categorie in categories if categorie.codeD == current.codeD])
    instances = MaterielInstance.query.order_by(MaterielInstance.idMateriel).filter_by(refMateriel=current.refMateriel).all()
    if (len(instances) <= 0):
        f2 = MaterielInstanceForm()
        return render_template("consultation.html",form = f, formInstance = f2, domaines=domaines, categories=categories, materiels=materiels, current_mat=current, instances=instances)
    instance = instances[0]
    f2 = MaterielInstanceForm(materielI=instance)
    return render_template("consultation.html",form = f, formInstance = f2, domaines=domaines, categories=categories, materiels=materiels, current_mat=current, instances=instances)

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
    ####liste_materiel = filtrer(liste_materiel, search, selected_domaine, selected_categorie) ### POUR REFACTORISER LE FILTRAGE

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
        materiel.complements = request.form["description"]
        materiel.codeD = request.form["domaine"]
        materiel.codeC = request.form["categorie"]

        db.session.commit()
        return redirect(url_for('consult'))
    return redirect(url_for('consult'))


@app.route('/consult/enregistrerinstance/', methods=['POST'])
def save_instance():
    hiddenref2 = request.form["hiddenref2"]
    hiddenrefMat = request.form["hiddenrefMat"]
    instance = MaterielInstance.query.filter_by(idMateriel=hiddenref2, refMateriel=hiddenrefMat).first()
    if instance:
        instance.datePeremption = request.form["datePeremption"]
        instance.qteRestante = request.form["quantiteRestante"]
        db.session.commit()
        return redirect(url_for('consult'))
    return redirect(url_for('consult'))

@app.route('/consult/supprimer/<int:id>')
def delete_material(id):
    materiel = MaterielGenerique.query.get(id)
    alertes = AlerteQuantite.query.filter_by(refMateriel=id).all()
    materiel_instances = MaterielInstance.query.filter_by(refMateriel=id).all()
    if materiel:
        for alerte in alertes:
            db.session.delete(alerte)
        for materiel_instance in materiel_instances:
            db.session.delete(materiel_instance)
        db.session.delete(materiel)
        db.session.commit()
        response = {'status': 'success'}
    else:
        response = {'status': 'error'}
    return jsonify(response)

@app.route('/consult/ouvreFDS/<int:id>')
def open_FDS(id):
    materiel = MaterielGenerique.query.get(id)
    if materiel and materiel.ficheFDS is not None:
        chemin = os.path.join('static','FDS')
        return send_from_directory(chemin, materiel.ficheFDS)

@app.route('/get_categories/')
def get_categories():
    selected_domaine = request.args.get('domaine')
    categories = Categorie.query.order_by(Categorie.nomC).all()
    if (selected_domaine):
        categories = [categorie for categorie in categories if categorie.codeD == int(selected_domaine)]
    categories = [categorie.serialize() for categorie in categories]
    return jsonify({'categories': categories})

@app.route('/commandes/creer_pdf/')
def creer_pdf_commandes():
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
        monPdf.cell(0, 10, txt="    Numéro de commande : "+str(commande.numeroCommande), ln=1, align="L")
        monPdf.cell(0, 10, txt="    Statut : "+commande.statut.nomStatut, ln=1, align="L")
        monPdf.cell(0, 10, txt="    Domaine : "+commande.materiel.domaine.nomD, ln=1, align="L")
        monPdf.cell(0, 10, txt="    Categorie : "+commande.materiel.categorie.nomC, ln=1, align="L")
        monPdf.cell(0, 10, txt="    Quantité commandée : "+str(commande.qteCommandee), ln=1, align="L")
        monPdf.cell(0, 10, txt="    Commande effectuée par : "+commande.utilisateur.nomUti, ln=1, align="L")

    monPdf.output("commandes.pdf")
    return jsonify({'nom_fichier' : 'commandes.pdf'})

@app.route('/consult/creer_pdf/')
def creer_pdf_materiel():
    #liste_materiel = Commande.query.order_by(Commande.dateCommande).all()
    #liste_materiel = filtrer(liste_commandes, request.args.get('search'), request.args.get('domaine'), request.args.get('categorie'))
    materielG = MaterielGenerique.query.get(request.args.get('ref'))
    monPdf = FPDF()
    monPdf.add_page()
    monPdf.set_font("Arial", size=30)
    monPdf.cell(0, 10, txt="Materiel", ln=1, align="C")
    monPdf.cell(0, 20, ln=1)
    monPdf.set_font("Arial", size=20)
    monPdf.cell(0, 10, txt=materielG.nomMateriel+" : ", ln=1, align="L")
    monPdf.set_font("Arial", size=10)
    monPdf.cell(0, 10, ln=1)

    monPdf.cell(0, 10, txt="    Référence : "+str(materielG.refMateriel), ln=1, align="L")
    monPdf.cell(0, 10, txt="    Domaine : "+materielG.domaine.nomD, ln=1, align="L")
    monPdf.cell(0, 10, txt="    Categorie : "+materielG.categorie.nomC, ln=1, align="L")
    monPdf.cell(0, 10, txt="    Quantité totale : "+str(materielG.qteMateriel), ln=1, align="L")
    monPdf.cell(0, 10, txt="    Quantité maximale : "+str(materielG.qteMax), ln=1, align="L")
    monPdf.cell(0, 10, txt="    Commentaire : "+materielG.complements, ln=1, align="L")

    instances = MaterielInstance.query.order_by(MaterielInstance.idMateriel).filter_by(refMateriel=materielG.refMateriel).all()
    for i in range(len(instances)):
        monPdf.cell(0, 5, ln=1)
        monPdf.cell(0, 10, txt="    Produit "+str(i+1), ln=1, align="L")
        monPdf.cell(0, 10, txt="        Date péremption : "+str(instances[i].datePeremption), ln=1, align="L")
        monPdf.cell(0, 10, txt="        Quantité restante : "+str(instances[i].qteRestante), ln=1, align="L")

    '''monPdf.set_font("Arial", size=15)
    monPdf.cell(0, 10, txt=commande.materiel.nomMateriel, ln=1, align="L")
    monPdf.set_font("Arial", size=10)
    monPdf.cell(0, 10, txt="Numéro de commande : "+str(commande.numeroCommande), ln=1, align="L")
    monPdf.cell(0, 10, txt="Statut : "+commande.statut.nomStatut, ln=1, align="L")
    monPdf.cell(0, 10, txt="Domaine : "+commande.materiel.domaine.nomD, ln=1, align="L")
    monPdf.cell(0, 10, txt="Categorie : "+commande.materiel.categorie.nomC, ln=1, align="L")
    monPdf.cell(0, 10, txt="Quantité commandée : "+str(commande.qteCommandee), ln=1, align="L")
    monPdf.cell(0, 10, txt="Commande effectuée par : "+commande.utilisateur.nomUti, ln=1, align="L")'''

    monPdf.output("materiel.pdf")
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
    return render_template("new_commande.html", form=f, alertes=getToutesLesAlertes())

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
    return render_template("ajout-materiel.html", form=f, alertes=getToutesLesAlertes())

@app.route("/save/materiel/", methods=("POST",))
def save_materiel():
    f = MaterielForm()
    ficheFDS_value = None
    if 'ficheFDS' in request.files:
        print("ficheFDS")
        file = request.files['ficheFDS']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('static','FDS',filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            ficheFDS_value = filename

    photo_value = None
    if 'photo' in request.files:
        image = request.files['photo']
        if image and image != "":
            photo_value = image.read()


    m = MaterielGenerique(
        refMateriel = 1 + db.session.query(db.func.max(MaterielGenerique.refMateriel)).scalar(),
        nomMateriel = f.nom.data,
        rangement = f.rangement.data,
        commentaire = f.commentaire.data,
        qteMateriel = 0,
        qteMax = f.quantite.data,
        unite = f.unite.data,
        complements = f.complements.data,
        seuilQte = f.seuil_quantite.data,
        seuilPeremption = f.seuil_peremption.data,
        codeD = f.domaine.data,
        codeC = f.categorie.data
    )
    if ficheFDS_value is not None:
        m.ficheFDS = ficheFDS_value
    if photo_value is not None:
        m.imageMateriel = photo_value
    db.session.add(m)
    db.session.commit()
    return redirect(url_for('consult'))

@app.route("/admin/home/")
@login_required
def admin_home():
    return render_template("admin.html", alertes=getToutesLesAlertes())
  
@app.route("/prof/home/")
@login_required
def prof_home():
    return render_template("prof.html", alertes=getToutesLesAlertes())

@app.route("/ecole/home/", methods=("GET","POST",))
@login_required
def ecole_home():
    return render_template("ecole.html", alertes=getToutesLesAlertes())

@app.route("/get_info_Materiel/<int:reference>", methods=["GET"])
def get_info_Materiel(reference):
    materiel = MaterielGenerique.query.get(reference)
    if materiel:
        liste_categories = Categorie.query.filter_by(codeD=materiel.codeD).all()
        liste_categories = [categorie.serialize() for categorie in liste_categories]
        liste_materiel_instance = MaterielInstance.query.filter_by(refMateriel=reference).all()
        liste_materiel_instance = [materiel_instance.serialize() for materiel_instance in liste_materiel_instance]
        image_data = materiel.get_image()
        materiel_info = {
            'reference': materiel.refMateriel,
            'nom': materiel.nomMateriel,
            'domaine': materiel.domaine.codeD,
            'categorie': materiel.categorie.codeC,
            'quantite_max': materiel.qteMax,
            'quantite_global': materiel.qteMateriel,
            'complements': materiel.complements,
            'image': image_data,
            'categories': liste_categories,
            'instances': liste_materiel_instance
        }
        return jsonify(materiel_info)
    else:
        return jsonify({'error': 'Materiel non trouvé'}), 404

@app.route("/get_info_Instance/<int:id>/<int:ref>", methods=["GET"])
def get_info_Materiel_Instance(id, ref):
    materiel_instance = MaterielInstance.query.get((id,ref))
    if materiel_instance:
        materiel_instance_info = materiel_instance.serialize()
        return jsonify(materiel_instance_info)
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
