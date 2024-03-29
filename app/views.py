"""Toute les routes et les Formulaires"""
import os
import json
import random
import string
from .app import app, db
from .models import AlerteQuantite, AlerteSeuil, Statut, MaterielGenerique, MaterielInstance, Utilisateur, Domaine, Categorie, Role, Commande, getToutesLesAlertes, getInstancesAlerte, PDF, getAdressesMail
from .forms import LoginForm, UtilisateurForm, UserForm, CommandeForm, MaterielForm, MaterielModificationForm, MaterielInstanceForm, LostPasswordForm, ReinitialisationMdpForm

from flask import jsonify, render_template, send_from_directory, url_for, redirect, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login/", methods=("GET","POST",))
def login():
    f = LoginForm()
    if request.method == "POST":
        if request.form["submit_button"] == "mdp":
            return redirect(url_for("lostpassword"))
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

@app.route('/login/lostpassword/', defaults={"mail":""})
@app.route('/login/lostpassword/<mail>')
def lostpassword(mail):
    def id_generator(size=8, chars=string.ascii_uppercase+string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))
    
    pwd = id_generator()
    f = LostPasswordForm(passwd=pwd, mail=mail)
    return render_template("lostpassword.html", form=f)

@app.route('/login/lostpassword/', methods=['POST'])
def lostpassword_update():
    f = LostPasswordForm()
    if f.mail_field.data in getAdressesMail():
        user_modified = Utilisateur.query.filter(Utilisateur.emailUti == f.mail_field.data).scalar()
        user_modified.mdp = f.pass_field.data
        db.session.commit()
        flash("Email envoyé avec succès !")
    else:
        flash("Utilisateur inconnu !")
    return redirect(url_for('login'))

@app.route('/reinitialisation_mot_de_passe/')
def reinitialisation_mdp():
    f = ReinitialisationMdpForm()
    return render_template("reinitialisation_mdp.html", form=f)

@app.route('/reinitialisation_mot_de_passe/', methods=['POST'])
def reinitialisation_mdp_update():
    f = ReinitialisationMdpForm()
    if f.email_field.data in getAdressesMail():
        if f.pass_field.data == f.confirm_password.data:
                user_modified = Utilisateur.query.filter(Utilisateur.emailUti == f.email_field.data).scalar()
                user_modified.mdp = f.confirm_password.data
                db.session.commit()
                flash("Email envoyé avec succès")
        else:
            flash("Le mot de passe doit être identique !")
    else:
        flash("Utilisateur inconnu !")
    return reinitialisation_mdp()

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
            'email': user.emailUti,
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
    if user:
        user_info = {
            'email': user.emailUti,
            'password': user.mdp
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
    f = MaterielModificationForm(materielG=current)
    f.set_domaine_choices([(domaine.codeD, domaine.nomD) for domaine in domaines])
    f.set_categorie_choices([(categorie.codeC, categorie.nomC) for categorie in categories if categorie.codeD == current.codeD])
    instances = MaterielInstance.query.order_by(MaterielInstance.idMateriel).filter_by(refMateriel=current.refMateriel).all()
    if (len(instances) <= 0):
        f2 = MaterielInstanceForm()
        return render_template("consultation.html",form = f, formInstance = f2, domaines=domaines, categories=categories, materiels=materiels, current_mat=current, instances=instances, alertes=getToutesLesAlertes())
    instance = instances[0]
    f2 = MaterielInstanceForm(materielI=instance)
    return render_template("consultation.html",form = f, formInstance = f2, domaines=domaines, categories=categories, materiels=materiels, current_mat=current, instances=instances, alertes=getToutesLesAlertes())

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
            alerteseuil = AlerteSeuil.query.filter_by(idMateriel=materiel_instance.idMateriel).all()
            for alerte in alerteseuil:
                db.session.delete(alerte)
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

@app.route("/imprimer_pdf/")
def imprimer_pdf():
    return send_from_directory('static/pdf/', request.args.get('chemin'))

@app.route('/commandes/creer_pdf/')
def creer_pdf_commandes():
            
    liste_commandes = Commande.query.order_by(Commande.dateCommande).all()
    liste_commandes = filtrer(liste_commandes, request.args.get('search'), request.args.get('domaine'), request.args.get('categorie'), request.args.get('statut'))
    monPdf = PDF()
    monPdf.set_title("commandes")
    monPdf.add_page()
    monPdf.set_font("Arial", size=30)
    monPdf.cell(0, 10, txt="Commandes", ln=1, align="C")
    monPdf.cell(0, 20, ln=1)
    monPdf.line(10, monPdf.get_y()-5, 200, monPdf.get_y()-5)
    monPdf.set_font("Arial", size=20)
    monPdf.cell(0, 10, txt="Liste de toutes les commandes : ", ln=1, align="L")
    monPdf.set_font("Arial", size=10)
    
    for i in range(len(liste_commandes)):
        ln = 0
        if i%3 == 0 and i!= 0:
            ln = 1
        monPdf.cell(70, 10, txt=" - "+liste_commandes[i].materiel.nomMateriel, ln=ln, align="L")

    monPdf.cell(0, 10, txt="", ln=1)
    monPdf.cell(0, 10, ln=1)
    monPdf.set_font_size(20)
    monPdf.line(10, monPdf.get_y()-5, 200, monPdf.get_y()-5)
    monPdf.cell(0, 10, txt="Détail des commandes")
    
    x,y = 120, monPdf.get_y()-60

    for i in range(len(liste_commandes)):
        if i%2==0:
            x-=100
            y+=80
        else:
            x+=100

        if (y+70 > monPdf.h-monPdf.b_margin):
            monPdf.add_page()
            y = 20

        monPdf.set_font("Arial", size=15)
        monPdf.text(x,y,liste_commandes[i].materiel.nomMateriel)
        monPdf.set_font("Arial", size=10)
        monPdf.text(x,y+10,"    Numéro de commande : "+str(liste_commandes[i].numeroCommande))
        monPdf.text(x,y+20,"    Statut : "+liste_commandes[i].statut.nomStatut)
        monPdf.text(x,y+30,"    Domaine : "+liste_commandes[i].materiel.domaine.nomD)
        monPdf.text(x,y+40,"    Categorie : "+liste_commandes[i].materiel.categorie.nomC)
        monPdf.text(x,y+50,"    Quantité commandée : "+str(liste_commandes[i].qteCommandee))
        monPdf.text(x,y+60,"    Commande effectuée par : "+liste_commandes[i].utilisateur.nomUti)

    monPdf.output("static/pdf/commandes.pdf")
    
    return jsonify({'nom_fichier' : "commandes.pdf"})

@app.route('/consult/creer_pdf/')
def creer_pdf_materiel():
    materielG = MaterielGenerique.query.get(request.args.get('ref'))    
    monPdf = PDF()
    monPdf.add_page()
    monPdf.set_font("Arial", size=30)
    monPdf.cell(0, 10, txt="Materiel", ln=1, align="C")
    monPdf.cell(0, 20, ln=1)
    monPdf.line(10, monPdf.get_y()-5, 200, monPdf.get_y()-5)
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

    monPdf.output("static/pdf/materiel.pdf")
    return jsonify({'nom_fichier' : 'materiel.pdf'})

@app.route('/alertes/creer_pdf/')
def creer_pdf_alertes():
    alertes = AlerteQuantite.query.all()
    alertes += AlerteSeuil.query.all()
    monPdf = PDF()
    monPdf.add_page()
    monPdf.set_font("Arial", size=30)
    monPdf.cell(0, 10, txt="Alertes", ln=1, align="C")
    monPdf.cell(0, 20, ln=1)

    monPdf.set_font("Arial", size=20)
    monPdf.line(10, monPdf.get_y()-5, 200, monPdf.get_y()-5)
    monPdf.cell(0, 10, txt="Liste de toutes les alertes", ln=1)
    monPdf.set_font("Arial", size=10)
    for i in range(len(alertes)):
        ln = 0
        if i%3 == 0 and i!= 0:
            ln = 1
        if type(alertes[i]) == AlerteQuantite:
            monPdf.cell(70, 10, txt="   - "+MaterielGenerique.query.get(alertes[i].refMateriel).nomMateriel, ln=ln, align="L")
        else:
            ref = MaterielInstance.query.filter(MaterielInstance.idMateriel == alertes[i].idMateriel)[0].refMateriel
            monPdf.cell(70, 10, txt="   - "+MaterielGenerique.query.get(ref).nomMateriel, ln=ln, align="L")

    monPdf.cell(0, 20, ln=1)
    monPdf.line(10, monPdf.get_y()-5, 200, monPdf.get_y()-5)
    monPdf.set_font("Arial", size=20)
    monPdf.cell(0, 10, txt="Détail des alertes", ln=1)
    monPdf.cell(0, 5, ln=1)
    monPdf.set_font("Arial", size=15)

    x,y = 120, monPdf.get_y()-20
    for i in range(len(alertes)):
        if i%2==0:
            x-=100
            y+=30
        else:
            x+=100
        if (y+10 > monPdf.h-monPdf.b_margin):
            monPdf.add_page()
            y = 20
        if type(alertes[i]) == AlerteQuantite:
            materiel = MaterielGenerique.query.get(alertes[i].refMateriel)
        else:
            materiel = MaterielGenerique.query.get(MaterielInstance.query.filter(MaterielInstance.idMateriel == alertes[i].idMateriel)[0].refMateriel)
        monPdf.set_font_size(15)
        monPdf.text(x, y, materiel.nomMateriel)
        monPdf.set_font_size(10)
        if type(alertes[i]) == AlerteSeuil:
            monPdf.text(x, y+10, txt="    Date Peremption : "+str(alertes[i].materiel.datePeremption))
        else:
            monPdf.text(x, y+10, txt="    Quantité restante : "+str(alertes[i].materiel.qteMateriel)) 

    monPdf.output("static/pdf/alertes.pdf")
    return jsonify({'nom_fichier' : 'alertes.pdf'})

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

@app.route("/commandes/")
def delivery():
    liste_commandes = Commande.query.all()
    liste_domaines = Domaine.query.order_by(Domaine.nomD).all()
    liste_categories = Categorie.query.distinct(Categorie.nomC).order_by(Categorie.nomC).all()
    liste_statuts = Statut.query.distinct(Statut.nomStatut).all()
    return render_template("gerer_commandes.html",liste_statuts=liste_statuts, liste_commandes=liste_commandes, liste_domaines=liste_domaines, liste_categories=liste_categories, alertes=getToutesLesAlertes())

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
    choice_id = request.args.get('refMateriel')
    if(choice_id):
        f = CommandeForm(choice_id)
    else:
        f = CommandeForm()
    f.materiel_field.choices = choix_materiel
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

@app.route("/notif/maj/")
def notif_maj():
    AlerteQuantite.query.delete()
    AlerteSeuil.query.delete()
    qte = 0
    listeMateriaux = MaterielGenerique.query.all()
    for materiel in listeMateriaux:
        materiel.seuilQte = 0 if materiel.seuilQte is None else materiel.seuilQte
        if materiel.qteMateriel <= materiel.seuilQte:
            alerteG = AlerteQuantite(
                idAlerteQ = 1 + db.session.query(db.func.coalesce(db.func.max(AlerteQuantite.idAlerteQ), 0)).scalar(),
                refMateriel = materiel.refMateriel,
                commentaire = "Quantité en dessous du seuil"
            )
            qte+=1
            db.session.add(alerteG)
    
    listeMateriauxInstance = MaterielInstance.query.all()
    for materielInstance in listeMateriauxInstance:
        if materielInstance.mat_generique.seuilPeremption==None:
            continue
        delai_en_jours = timedelta(days=materielInstance.mat_generique.seuilPeremption)
        date_peremption_limite = datetime.combine(materielInstance.datePeremption, datetime.min.time()) - delai_en_jours
        if date_peremption_limite <= datetime.utcnow():
            idMateriel_value = materielInstance.idMateriel
            refMateriel_value = materielInstance.refMateriel
            existing_instance = MaterielInstance.query.get((idMateriel_value, refMateriel_value))
            if existing_instance:
                newid = 1 + db.session.query(db.func.coalesce(db.func.max(AlerteSeuil.idAlerteS), 0)).scalar()
                alerteS = AlerteSeuil(
                    idAlerteS=newid,
                    idMateriel=idMateriel_value,
                    commentaire="Date de péremption proche"
                )
                qte += 1
                db.session.add(alerteS)
    db.session.commit()
    return jsonify({'qte': qte})

@app.route("/notifications/")
def notifications():
    return render_template("notifications.html", alertes=getToutesLesAlertes(), instances=getInstancesAlerte(), nb=len(getInstancesAlerte()))

@app.route("/alertes/qte/get_info/", methods=["GET"])
def get_alerte_qte_info():
    ida = request.args.get("ida")
    numm = request.args.get("numm")
    alerte = AlerteQuantite.query.get((ida,numm))
    if alerte:
        alerte_info = alerte.serialize()
        return jsonify(alerte_info)
    else:
        return jsonify({'error': 'Commande non trouvé'}), 404
    
@app.route("/alertes/seuil/get_info/", methods=["GET"])
def get_alerte_seuil_info():
    ida = request.args.get("ida")
    numm = request.args.get("numm")
    alerte = AlerteSeuil.query.get((ida,numm))
    if alerte:
        alerte_info = alerte.serialize()
        return jsonify(alerte_info)
    else:
        return jsonify({'error': 'Commande non trouvé'}), 404