from datetime import date
import click
from app.app import db, app

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''

    # création de toutes les tables
    db.create_all()

    # Chargement de notre jeu de données
    import yaml
    data = yaml.safe_load(open(filename))

    # Import des modèles
    from .models import Role, Utilisateur, Domaine, Categorie, Materiel, Commande, Commander

    # Création des différentes tables de notre base de données
    # {Categorie:[{code: 1, nom:"", code_domaine:1}, {...}]}

    liste_roles = data["Role"]
    liste_users = data["Utilisateur"]
    liste_domaines = data["Domaine"]
    liste_categories = data["Categorie"]
    liste_materiels = data["Materiel"]
    liste_commandes = data["Commande"]
    liste_commander = data["Commander"]

    for dico_role in liste_roles:
        role = Role(intitule=dico_role["intitule"])
        db.session.add(role)
    db.session.commit()

    for dico_domaines in liste_domaines:
        domaine = Domaine(nom=dico_domaines["nomD"])
        db.session.add(domaine)
    db.session.commit()

    for dico_categories in liste_categories:
        categorie = Categorie(code=dico_categories["codeC"],
                              nom=dico_categories["nomC"],
                              code_domaine=dico_categories["codeD"])
        db.session.add(categorie)
    db.session.commit()

    users = dict()
    for dico_users in liste_users:
        user_name = dico_users["nomUti"]
        if user_name not in users:
            o = Utilisateur(nom=user_name,
                            prenom=dico_users["prenomUti"],
                            email=dico_users["emailUti"],
                            tel=dico_users["telUti"],
                            id_role=dico_users["idRole"])
            db.session.add(o)
            users[user_name] = o
    db.session.commit()

    materials = dict()
    for dico_materials in liste_materiels:
        material_ref = dico_materials["refMateriel"]
        if material_ref not in materials:
            date_peremption_str = dico_materials["datePeremption"]
            date_peremption = None
            if date_peremption_str is not None:
                d_peremption = date_peremption_str.split("-")
                date_peremption = date(int(d_peremption[0]),
                                       int(d_peremption[1]),
                                       int(d_peremption[2]))
            o = Materiel(reference=material_ref,
                         nom=dico_materials["nomMateriel"],
                         rangement=dico_materials["precisionMateriel"],
                         commentaire=dico_materials["commentaire"],
                         quantite_globale=dico_materials["qteMateriel"],
                         quantite_max=dico_materials["qteMax"],
                         unite=dico_materials["unite"],
                         quantite_restante=dico_materials["qteRestante"],
                         complements=dico_materials["complements"],
                         fiche_fds=dico_materials["ficheFDS"],
                         date_peremption=date_peremption,
                         seuil_quantite=dico_materials["seuilQte"],
                         seuil_peremption=dico_materials["seuilPeremption"],
                         code_categorie=dico_materials["codeC"],
                         code_domaine=dico_materials["codeD"])
            db.session.add(o)
            materials[material_ref] = o
    db.session.commit()

    commandes = dict()
    for dico_commandes in liste_commandes:
        num_commande = dico_commandes["numeroCommande"]
        if num_commande not in commandes:
            date_commande_str = dico_commandes["dateCommande"]
            date_reception_str = dico_commandes["dateReception"]
            date_commande = None
            date_reception = None
            if date_peremption_str is not None:
                d_commande = date_commande_str.split("-")
                d_reception = date_reception_str.split("-")
                date_commande = date(int(d_commande[0]), int(d_commande[1]),
                                     int(d_commande[2]))
                date_reception = date(int(d_reception[0]), int(d_reception[1]),
                                      int(d_reception[2]))
            o = Commande(numero=dico_commandes["numeroCommande"],
                         date_commande=date_commande,
                         date_reception=date_reception,
                         statut=dico_commandes["statut"],
                         id_util=dico_commandes["idUti"],
                         ref_materiel=dico_commandes["refMateriel"])
            db.session.add(o)
            commandes[num_commande] = o
    db.session.commit()

    commander = dict()
    for dico_commander in liste_commander:
        num_comm = dico_commander["numeroCommande"]
        if num_comm not in commander:
            o = Commander(numero_commande=num_comm,
                          quantite_commandee=dico_commander["qteCommandee"],
                          id_util=dico_commander["idUti"],
                          ref_materiel=dico_commander["refMateriel"])
            db.session.add(o)
            commander[num_comm] = o
    db.session.commit()
