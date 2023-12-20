"""Lien avec la Base de données"""

from base64 import b64encode
from .app import db, login_manager
from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = "ROLE"
    idRole = db.Column(db.Integer, primary_key=True)
    intitule = db.Column(db.String(100))

    def __repr__(self):
        return "<Role (%d) %s>" % (self.id, self.intitule)


class Utilisateur(db.Model, UserMixin):
    __tablename__ = "UTILISATEUR"
    idUti = db.Column(db.Integer, primary_key=True)
    nomUti = db.Column(db.String(100))
    prenomUti = db.Column(db.String(100))
    emailUti = db.Column(db.String(100), unique=True)
    modifications = db.Column(db.Boolean)
    mdp = db.Column(db.String(100))
    idRole = db.Column(db.Integer, db.ForeignKey("ROLE.idRole"))
    role = db.relationship("Role",
                           backref=db.backref("utilisateurs", lazy="dynamic"))

    def __repr__(self):
        return "<Utilisateur (%d) %s %r>" % (self.idUti, self.nomUti, self.prenomUti)

    def is_prof(self):
        """Vérifie si l'utilisateur passé en paramètres est un professeur

        Args:
            user (Utilisateur): un utilisateur

        Returns:
            boolean: True si l'utilisateur est un professeur, False sinon
        """
        role = Role.query.filter(Role.intitule == "Professeur").scalar()
        return role.idRole == self.idRole

    def is_admin(self):
        """Vérifie si l'utilisateur passé en paramètres est un admin

        Args:
            user (Utilisateur): un utilisateur

        Returns:
            boolean: True si l'utilisateur est un admin, False sinon
        """
        role = Role.query.filter(Role.intitule == "Administrateur").scalar()
        return role.idRole == self.idRole

    def is_etablissement(self):
        """Vérifie si l'utilisateur passé en paramètres est un établissement

        Args:
            user (Utilisateur): un utilisateur

        Returns:
            boolean: True si l'utilisateur est un établissement, False sinon
        """
        role = Role.query.filter(Role.intitule == "Etablissement").scalar()
        return role.idRole == self.idRole
    
    def get_id(self):
        return self.idUti

    def get_role(self):
        return Role.query.filter(Role.idRole == self.idRole).scalar()


class Domaine(db.Model):
    __tablename__ = "DOMAINE"
    codeD = db.Column(db.Integer, primary_key=True)
    nomD = db.Column(db.String(100))

    def __repr__(self):
        return "<Domaine (%d) %s>" % (self.codeD, self.nomD)


class Categorie(db.Model):
    __tablename__ = "CATEGORIE"
    codeC = db.Column(db.Integer, primary_key=True)
    nomC = db.Column(db.String(100))
    codeD = db.Column(db.Integer, db.ForeignKey("DOMAINE.codeD"))
    domaine = db.relationship("Domaine",
                              backref=db.backref("categories", lazy="dynamic"))

    __table_args__ = (db.UniqueConstraint('codeC', 'codeD'),)

    def serialize(self):
        return {
            'codeC': self.codeC,
            'nom': self.nomC,
            'codeD': self.codeD,
        }

    def __repr__(self):
        return "<Categorie (%d) %s %r>" % (self.codeC, self.nomC, self.codeD)


class MaterielGenerique(db.Model):
    __tablename__ = "MATERIELGENERIQUE"
    refMateriel = db.Column(db.Integer, primary_key=True)
    nomMateriel = db.Column(db.String(100))
    rangement = db.Column(db.String(100))
    commentaire = db.Column(db.String(100))
    qteMateriel = db.Column(db.Float)
    unite = db.Column(db.String(100))
    qteMax = db.Column(db.Float)
    complements = db.Column(db.String(500))
    ficheFDS = db.Column(db.LargeBinary)
    seuilQte = db.Column(db.Integer)
    seuilPeremption = db.Column(db.Integer)
    imageMateriel = db.Column(db.LargeBinary)
    codeC = db.Column(db.Integer, db.ForeignKey("CATEGORIE.codeC"))
    codeD = db.Column(db.Integer, db.ForeignKey("DOMAINE.codeD"))
    categorie = db.relationship("Categorie",
                                backref=db.backref("matériels",
                                                   lazy="dynamic"))
    domaine = db.relationship("Domaine",
                              backref=db.backref("matériels", lazy="dynamic"))

    def get_image(self):
        if self.imageMateriel is not None:
            return b64encode(self.imageMateriel).decode("utf-8")
        else:
            default_image_path = "static/images/black_square.png"
            with open(default_image_path, 'rb') as f:
                default_image_data = f.read()
            return b64encode(default_image_data).decode("utf-8")

    def serialize(self):
        return {
            'reference': self.reference,
            'nom': self.nom,
            'quantite_max': self.quantite_max,
            'unite': self.unite,
            'quantite': self.quantite,
            'complements': self.complements,
            'code_categorie': self.code_categorie,
            'code_domaine': self.code_domaine,
            'image': self.get_image(),
        }

    def __repr__(self):
        return "<Materiel (%d)>" % (self.refMateriel)


class MaterielInstance(db.Model):
    __tablename__ = "MATERIELINSTANCE"
    idMateriel = db.Column(db.Integer, primary_key=True)
    qteRestante = db.Column(db.Float)
    datePeremption = db.Column(db.Float)
    refMateriel = db.Column(db.Integer, db.ForeignKey("MATERIELGENERIQUE.refMateriel"), primary_key=True)
    mat_generique = db.relationship("MaterielGenerique",
                                backref=db.backref("matériels",
                                                   lazy="dynamic"))

    def serialize(self):
        return {
            'reference': self.idMateriel,
            'quantite_restante': self.qteRestante,
            'date_peremption': self.datePeremption,
        }

    def __repr__(self):
        return "<Materiel (%d)>" % (self.idMateriel)


class Statut(db.Model):
    __tablename__ = "STATUT"
    idStatut = db.Column(db.Integer, primary_key=True)
    nomStatut = db.Column(db.String)

    def __repr__(self):
        return "<Statut (%d) %s>" % (self.idStatut, self.nomStatut)


class Commande(db.Model):
    __tablename__ = "COMMANDE"
    numeroCommande = db.Column(db.Integer, primary_key=True)
    dateCommande = db.Column(db.Date)
    dateReception = db.Column(db.Date)
    qteCommandee = db.Column(db.Integer)
    idStatut = db.Column(db.Integer, db.ForeignKey("STATUT.idStatut"))
    statut = db.relationship("Statut", backref=db.backref("statuts", lazy="dynamic"))
    idUti = db.Column(db.Integer, db.ForeignKey("UTILISATEUR.idUti"))
    refMateriel = db.Column(db.Integer, db.ForeignKey("MATERIELGENERIQUE.refMateriel"))
    utilisateur = db.relationship("Utilisateur",
                                  backref=db.backref("commandes",
                                                     lazy="dynamic"))
    materiel = db.relationship("MaterielGenerique",
                               backref=db.backref("commandes", lazy="dynamic"))
    
    def serialize(self):
        return {
            'numero': self.numero,
            'nom': self.materiel.nom,
            'domaine': self.materiel.domaine.nom,
            'categorie': self.materiel.categorie.nom,
            'statut': self.statut,
            'quantite': self.quantite_commandee,
            'unite': self.materiel.unite,
            'user': self.utilisateur.nom
        }


    def __repr__(self):
        return "<Commande (%d) %s %r %e %c %d>" % (self.numeroCommande, self.dateCommande, self.idStatut, self.dateReception, self.idUti, self.refMateriel)


class AlerteSeuil(db.Model):
    __tablename__ = "ALERTESEUIL"
    idAlerteS = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String(150))
    idMateriel = db.Column(db.Integer,
                             db.ForeignKey("MATERIELINSTANCE.idMateriel"),
                             primary_key=True)
    materiel = db.relationship("MaterielInstance",
                               backref=db.backref("alertes", lazy="dynamic"))

    def __repr__(self):
        return "<Alerte (%d) %s %r>" % (self.idAlertes, self.commentaire, self.idMateriel)


class AlerteQuantite(db.Model):
    __tablename__ = "ALERTEQUANTITE"
    idAlerteQ = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String(150))
    refMateriel = db.Column(db.Integer,
                             db.ForeignKey("MATERIELGENERIQUE.refMateriel"),
                             primary_key=True)
    materiel = db.relationship("MaterielGenerique",
                               backref=db.backref("alertes", lazy="dynamic"))

    def __repr__(self):
        return "<Alerte (%d) %s %r>" % (self.idAlerteQ, self.commentaire, self.refMateriel)


@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

def filter_commands(txt, domaine, categorie, statut, commandes):
    liste_materiel = []
    for materiel in MaterielGenerique.query.all():
        if txt.upper() in materiel.nom.upper():
            liste_materiel.append(materiel)
    liste_commandes = []

    for commande in commandes:
        if commande.materiel in liste_materiel:
            if commande.materiel.domaine.nom == domaine or domaine == "Domaine":
                if commande.materiel.categorie.nom == categorie or categorie == "Categorie":
                    if commande.statut == statut or statut == "Statut":
                        liste_commandes.append(commande)

    return liste_commandes

def getToutesLesAlertes():
    res = []
    for aQte in AlerteQuantite.query.all():
        res.append(aQte.commentaire + " pour " + MaterielGenerique.query.get(aQte.refMateriel).nomMateriel + ".")
    for aSl in AlerteSeuil.query.all():
        res.append(aSl.commentaire + " pour " + MaterielInstance.query.get(aSl.idMateriel).nomMateriel + ".")
    print(res)
    return res
