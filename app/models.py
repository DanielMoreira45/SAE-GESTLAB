"""Lien avec la Base de données"""

from .app import app, db, login_manager
from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    intitule = db.Column(db.String(100))

    def __repr__(self):
        return "<Role (%d) %s>" % (self.id, self.intitule)


class Utilisateur(db.Model, UserMixin):
    __tablename__ = "utilisateur"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    id_role = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", backref=db.backref("utilisateurs", lazy="dynamic"))

    def __repr__(self):
        return "<Utilisateur (%d) %s %r>" % (self.id, self.nom, self.prenom)

    def is_prof(self):
        """Vérifie si l'utilisateur passé en paramètres est un professeur

        Args:
            user (Utilisateur): un utilisateur

        Returns:
            boolean: True si l'utilisateur est un professeur, False sinon
        """
        role = Role.query.filter(Role.intitule == "Professeur").scalar()
        return role.id == self.id_role

    def is_admin(self):
        """Vérifie si l'utilisateur passé en paramètres est un admin

        Args:
            user (Utilisateur): un utilisateur

        Returns:
            boolean: True si l'utilisateur est un admin, False sinon
        """
        role = Role.query.filter(Role.intitule == "Administrateur").scalar()
        return role.id == self.id_role


    def is_etablissement(self):
        """Vérifie si l'utilisateur passé en paramètres est un établissement

        Args:
            user (Utilisateur): un utilisateur

        Returns:
            boolean: True si l'utilisateur est un établissement, False sinon
        """
        role = Role.query.filter(Role.intitule == "Etablissement").scalar()
        return role.id == self.id_role
    
    def get_id(self):
        return self.id


class Domaine(db.Model):
    __tablename__ = "domaine"
    code = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))

    def __repr__(self):
        return "<Domaine (%d) %s>" % (self.code, self.nom)


class Categorie(db.Model):
    __tablename__ = "categorie"
    code = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    code_domaine = db.Column(db.Integer, db.ForeignKey("domaine.code"))
    domaine = db.relationship("Domaine",
                              backref=db.backref("categories", lazy="dynamic"))

    __table_args__ = (db.UniqueConstraint('code', 'code_domaine'),)

    def __repr__(self):
        return "<Categorie (%d) %s %r>" % (self.code, self.nom, self.code_domaine)


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

    def __repr__(self):
        return "<Materiel (%d) %s %r %p %c %q>" % (self.reference, self.nom, self.rangement, self.date_peremption, self.commentaire, self.quantite_globale)


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

    def __repr__(self):
        return "<Commande (%d) %s %r %p %c %d>" % (self.numero, self.date_commande, self.statut, self.date_reception, self.id_util, self.ref_materiel)


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

    def __repr__(self):
        return "<Commander (%d) %s %r %p>" % (self.numero_commande, self.quantite_commandee, self.id_util, self.ref_materiel)


class Alerte(db.Model):
    __tablename__ = "alerte"
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.String(150))
    ref_materiel = db.Column(db.Integer,
                             db.ForeignKey("materiel.reference"),
                             primary_key=True)
    materiel = db.relationship("Materiel",
                               backref=db.backref("alertes", lazy="dynamic"))

    def __repr__(self):
        return "<Alerte (%d) %s %r>" % (self.id, self.commentaire, self.ref_materiel)

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

def get_liste_materiel():
    liste_mat = []
    materiel_query = Materiel.query.all()
    for mat in materiel_query:
        liste_mat.append((mat.reference, mat.nom))
    return liste_mat