"""Lien avec la Base de données"""

from .app import db


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    intitule = db.Column(db.String(100))


class Utilisateur(db.Model):
    __tablename__ = "utilisateur"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tel = db.Column(db.String(100))
    id_role = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", backref=db.backref("utilisateurs", lazy="dynamic"))

class Domaine(db.Model):
    __tablename__ = "domaine"
    code = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))


class Categorie(db.Model):
    __tablename__ = "categorie"
    code = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    code_domaine = db.Column(db.Integer, db.ForeignKey("domaine.code"))
    domaine = db.relationship("Domaine",
                              backref=db.backref("categories", lazy="dynamic"))

    __table_args__ = (db.UniqueConstraint('code', 'code_domaine'),)


class Materiel(db.Model):
    __tablename__ = "materiel"
    reference = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    rangement = db.Column(db.String(100))
    commentaire = db.Column(db.String(100))
    quantite_globale = db.Column(db.Integer)
    quantite_max = db.Column(db.Integer)
    unite = db.Column(db.String(100))
    quantite_restante = db.Column(db.Float)
    complements = db.Column(db.String(500))
    fiche_fds = db.Column(db.LargeBinary)
    date_peremption = db.Column(db.Date)
    seuil_quantite = db.Column(db.Integer)
    seuil_peremption = db.Column(db.Integer)
    code_categorie = db.Column(db.Integer, db.ForeignKey("categorie.code"))
    code_domaine = db.Column(db.Integer, db.ForeignKey("domaine.code"))
    categorie = db.relationship("Categorie",
                                backref=db.backref("matériels",
                                                   lazy="dynamic"))
    domaine = db.relationship("Domaine",
                              backref=db.backref("matériels", lazy="dynamic"))


class Commande(db.Model):
    __tablename__ = "commande"
    numero = db.Column(db.Integer, primary_key=True)
    date_commande = db.Column(db.Date)
    date_reception = db.Column(db.Date)
    statut = db.Column(db.String(100))
    id_util = db.Column(db.Integer, db.ForeignKey("utilisateur.id"), primary_key=True)
    ref_materiel = db.Column(db.Integer, db.ForeignKey("materiel.reference"), primary_key=True)
    utilisateur = db.relationship("Utilisateur",
                                  backref=db.backref("commandes",
                                                     lazy="dynamic"))
    materiel = db.relationship("Materiel",
                               backref=db.backref("commandes", lazy="dynamic"))


class Commander(db.Model):
    __tablename__ = "commander"
    numero_commande = db.Column(db.Integer, primary_key=True)
    quantite_commandee = db.Column(db.Integer)
    id_util = db.Column(db.Integer,
                        db.ForeignKey("utilisateur.id"),
                        primary_key=True)
    ref_materiel = db.Column(db.Integer,
                             db.ForeignKey("materiel.reference"),
                             primary_key=True)
    utilisateur = db.relationship("Utilisateur",
                                  backref=db.backref("commandes_effectuees",
                                                     lazy="dynamic"))
    materiel = db.relationship("Materiel",
                               backref=db.backref("commandes_effectuees",
                                                  lazy="dynamic"))
