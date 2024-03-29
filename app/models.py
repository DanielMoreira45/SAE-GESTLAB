"""Lien avec la Base de données"""

from base64 import b64encode
from .app import db, login_manager
from flask_login import UserMixin
from fpdf import FPDF

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
            'nomC': self.nomC,
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
    ficheFDS = db.Column(db.String(100))
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
            'reference': self.refMateriel,
            'nom': self.nomMateriel,
            'quantite_max': self.qteMax,
            'unite': self.unite,
            'quantite': self.qteMateriel,
            'complements': self.complements,
            'code_categorie': self.codeC,
            'code_domaine': self.codeD,
            'image': self.get_image(),
        }

    def __repr__(self):
        return "<Materiel (%d)>" % (self.refMateriel)


class MaterielInstance(db.Model):
    __tablename__ = "MATERIELINSTANCE"
    idMateriel = db.Column(db.Integer, primary_key=True)
    qteRestante = db.Column(db.Float)
    datePeremption = db.Column(db.Date)
    refMateriel = db.Column(db.Integer, db.ForeignKey("MATERIELGENERIQUE.refMateriel"), primary_key=True)
    mat_generique = db.relationship("MaterielGenerique",
                                backref=db.backref("matériels",
                                                   lazy="dynamic"))

    def serialize(self):
        return {
            'nomMateriel': self.mat_generique.nomMateriel,
            'unite': self.mat_generique.unite,
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
    utilisateur = db.relationship("Utilisateur", backref=db.backref("commandes", lazy="dynamic"))
    materiel = db.relationship("MaterielGenerique", backref=db.backref("commandes", lazy="dynamic"))
    
    def serialize(self):
        return {
            'numero': self.numeroCommande,
            'nom': self.materiel.nomMateriel,
            'domaine': self.materiel.domaine.nomD,
            'categorie': self.materiel.categorie.nomC,
            'statut': self.statut.nomStatut,
            'quantite': self.qteCommandee,
            'unite': self.materiel.unite,
            'user': self.utilisateur.nomUti,
            'image': self.materiel.get_image()
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

    def serialize(self):
        return {
            'id': self.idAlerteS,
            'nom' : self.materiel.mat_generique.nomMateriel,
            'commentaire': self.commentaire,
            'idMateriel': self.idMateriel,
            'qteRestante' : self.materiel.qteRestante,
            'datePeremption' : self.materiel.datePeremption,
            'refMateriel': self.materiel.refMateriel,
            'seuilPeremption': self.materiel.mat_generique.seuilPeremption
        }

    def __repr__(self):
        return "<Alerte (%d) %s %r>" % (self.idAlerteS, self.commentaire, self.idMateriel)


class AlerteQuantite(db.Model):
    __tablename__ = "ALERTEQUANTITE"
    idAlerteQ = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String(150))
    refMateriel = db.Column(db.Integer,
                             db.ForeignKey("MATERIELGENERIQUE.refMateriel"),
                             primary_key=True)
    materiel = db.relationship("MaterielGenerique",
                               backref=db.backref("alertes", lazy="dynamic"))

    def serialize(self):
        return {
            'id': self.idAlerteQ,
            'nom' : self.materiel.nomMateriel,
            'commentaire': self.commentaire,
            'refMateriel': self.refMateriel,
            'qteMax' : self.materiel.qteMax,
            'qteMateriel' : self.materiel.qteMateriel,
            'unite' : self.materiel.unite,
            'seuil' : self.materiel.seuilQte
        }

    def __repr__(self):
        return "<Alerte (%d) %s %r>" % (self.idAlerteQ, self.commentaire, self.refMateriel)


@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

def getAlertesQuantite():
    res = []
    for alerte_qte in AlerteQuantite.query.all():
        res.append(alerte_qte.commentaire +
                   " pour " +
                   MaterielGenerique.query.get(alerte_qte.refMateriel).nomMateriel +
                   ".")
    return res

def getAlertesSeuil():
    res = []
    # for mat_inst in MaterielInstance.query.all():
    #     res.append(AlerteSeuil.query.get(mat_inst.idMateriel).commentaire +
    #                 " pour " +
    #                 mat_inst.nomMateriel +
    #                 ".")
    for alerte_seuil in AlerteSeuil.query.all():
        ref_materiel = MaterielInstance.query.filter(MaterielInstance.idMateriel == alerte_seuil.idMateriel)[0].refMateriel
        nom_materiel = MaterielGenerique.query.get(ref_materiel).nomMateriel
        res.append(alerte_seuil.commentaire +
                   " pour " +
                   nom_materiel +
                   ".")
    return res

def getToutesLesAlertes():
    return getAlertesQuantite() + getAlertesSeuil()

def getInstancesAlerte():
    return AlerteQuantite.query.all() + AlerteSeuil.query.all()

class PDF(FPDF):

    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Print centered page number
        self.cell(0, 10, 'Gestlab 2023-2024', 0, 0, 'L')
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'R')

def getAdressesMail():
    users = Utilisateur.query.all()
    emails = []
    for user in users:
        emails.append(user.emailUti)
    return emails
