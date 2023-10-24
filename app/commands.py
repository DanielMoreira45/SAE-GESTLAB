import click
from .app import db

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
        role = Role(nom=dico_role["nom"])
        db.session.add(role)
    db.session.commit()

    for dico_domaines in liste_domaines:
        domaine = Domaine(nom=dico_domaines["nom"])
        db.session.add(domaine)
    db.session.commit()

    for dico_categories in liste_categories:
        categorie = Categorie(nom=dico_categories["nom"])
        db.session.add(categorie)
    db.session.commit()

    users = dict()
    for dico_users in liste_users:
        user_name = dico_users["nom"]
        if user_name not in users:
            o = Utilisateur(nom=user_name, 
                            prenom=dico_users["prenom"], 
                            email=dico_users["email"], 
                            tel=dico_users["tel"], 
                            id_role=dico_users["id_role"])
            db.session.add(o)
            users[user_name] = o
    db.session.commit()

    materials = dict()
    for dico_materials in liste_materiels:
        material_ref = dico_materials["nom"]
        if material_ref not in materials:
            o = Materiel(reference=material_ref, 
                         nom=dico_materials["nom"], 
                         rangement=dico_materials["rangement"],
                         commentaire=dico_materials["commentaire"],
                         quantite_globale=dico_materials["quantite_globale"],
                         quantite_max=dico_materials["quantite_max"],
                         unite=dico_materials["unite"],
                         quantite_restante=dico_materials["quantite_restante"],
                         complements=dico_materials["complements"],
                         fiche_fds=dico_materials["fiche_fds"],
                         date_peremption=dico_materials["date_peremption"],
                         seuil_quantite=dico_materials["seuil_quantite"],
                         seuil_peremption=dico_materials["seuil_peremption"],
                         code_categorie=dico_materials["code_categorie"],
                         code_domaine=dico_materials["code_domaine"])
            db.session.add(o)
            materials[material_ref] = o
    db.session.commit()

    commandes = dict()
    for dico_commandes in liste_commandes:
        num_commande = dico_commandes["numero"]
        if num_commande not in commandes:
            o = Commande(date_commande=dico_commandes["date_commande"],
                         date_reception=dico_commandes["date_reception"],
                         statut=dico_commandes["statut"],
                         id_util=dico_commandes["id_util"],
                         ref_materiel=dico_commandes["ref_materiel"])
            db.session.add(o)
            commandes[num_commande] = o
    db.session.commit()

    commander = dict()
    for dico_commander in liste_commander:
        num_comm = dico_commander["numero_commande"]
        if num_comm not in commander:
            o = Commander(numero_commande=num_comm, 
                          quantite_commandee=dico_commander["quantitee_commandee"],
                          id_util=dico_commander["id_util"],
                          ref_materiel=dico_commander["ref_materiel"])
            db.session.add(o)
            commander[num_comm] = o
    db.session.commit()
