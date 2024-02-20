from flask_wtf import FlaskForm
from wtforms import DateField, FileField, StringField, HiddenField, PasswordField, SelectField, RadioField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, NumberRange, Email
from .models import Utilisateur

"Formulaires de l'application"

class MaterielModificationForm(FlaskForm):
    """Formulaire de modification du matériel."""

    nom = StringField('Nom', validators=[DataRequired()])
    hiddenref = HiddenField('hiddenref')
    reference = StringField('Référence', validators=[DataRequired()])
    rangement = StringField('Rangement', validators=[DataRequired()])
    commentaire = StringField('Commentaire', validators=[DataRequired()])
    domaine = SelectField('Domaine', validators=[DataRequired()])
    categorie = SelectField('Catégorie', validators=[DataRequired()])
    quantiteTot = IntegerField('Quantité totale', validators=[DataRequired()])
    quantiteMax = IntegerField('Quantité maximale', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    seuil_peremption = IntegerField('Seuil de péremption', validators=[DataRequired()])
    seuil_quantite = IntegerField('Seuil de quantité', validators=[DataRequired()])

    def __init__(self, materielG=None, *args, **kwargs):
        super(MaterielModificationForm, self).__init__(*args, **kwargs)
        
        if materielG:
            self.nom.default = materielG.nomMateriel
            self.reference.default = materielG.refMateriel
            self.quantiteTot.default = materielG.qteMateriel
            self.description.default = materielG.complements
            self.hiddenref.default = materielG.refMateriel
            self.quantiteMax.default = materielG.qteMax
            self.categorie.default = materielG.categorie.codeC
            self.domaine.default = materielG.domaine.codeD
            self.rangement.default = materielG.rangement
            self.commentaire.default = materielG.commentaire
            self.seuil_peremption.default = materielG.seuilPeremption
            self.seuil_quantite.default = materielG.seuilQte
        self.process()

    def set_domaine_choices(self, choices):
        self.domaine.choices = choices

    def set_categorie_choices(self, choices):
        self.categorie.choices = choices

class MaterielInstanceForm(FlaskForm):
    """Formulaire d'ajout d'une instance de matériel."""

    reference = HiddenField('Référence')
    hiddenrefMat = HiddenField('RéférenceMat')
    datePeremption = DateField('Date de péremption', validators=[DataRequired()])
    quantiteRes = IntegerField('Quantité restante', validators=[DataRequired()])

    def __init__(self, materielI=None, *args, **kwargs):
        super(MaterielInstanceForm, self).__init__(*args, **kwargs)
        if materielI:
            self.datePeremption.default = materielI.datePeremption
            self.quantiteRes.default = materielI.qteRestante
            self.reference.default = materielI.idMateriel
            self.hiddenrefMat.default = materielI.mat_generique.refMateriel

class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    password_incorrect = ""
    next = HiddenField()

    def get_authenticated_user(self):
        user = Utilisateur.query.filter_by(emailUti=self.email.data).first()
        if user and user.mdp == self.password.data:
            return user
    
    def has_content(self):
        return self.password.data != "" or self.email.data != ""
    
    def show_password_incorrect(self):
        self.password_incorrect = "Email ou mot de passe incorrect"

# Permet la modification de l'utilisateur
class UserForm(FlaskForm):
    id = HiddenField('id')
    email = HiddenField('email')
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    id_role = SelectField('role', validators=[DataRequired()], choices=[(1, 'Administrateur'), (2, 'Professeur'), (3, 'Etablissement')])
    modifications = RadioField('modifications', validators=[DataRequired()])

# Permet l'insertion de l'utilisateur
class UtilisateurForm(FlaskForm):
    idUti = HiddenField('iduti')
    idRole = HiddenField('idrole')
    nomUti = StringField('Nom', validators=[DataRequired()])
    prenomUti = StringField('Prénom', validators=[DataRequired()])
    emailUti = StringField('Email', validators=[DataRequired()])
    mdp = PasswordField('Mot de Passe', validators=[DataRequired()])
    role = SelectField('Rôle', choices=[(1, 'Administrateur'), (2, 'Professeur'), (3, 'Etablissement')])
    modif = RadioField('Droit de Modification', choices=[(True, 'Oui'), (False, 'Non')], validators=[DataRequired()])

class CommandeForm(FlaskForm):
    materiel_field = SelectField('Matériel', validators=[DataRequired("Merci de sélectionner une option.")])
    quantity_field = IntegerField("Quantité", validators=[DataRequired(), NumberRange(1, 1000)], default=1)

class MaterielForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    photo = FileField('Photo')
    lesD = [(1, 'Appareillage'),
            (2, 'Verrerie et associés'),
            (3, 'Produits Chimiques'),
            (4, 'Matériel de Laboratoire'),
            (5, 'Média'),
            (6, 'Matériel Électrique')]
    lesC = [(1, 'Observation'),
            (2, 'Mesures'),
            (3, 'ExAO'),
            (4, 'Multimédia'),
            (5, 'Expérimentation'),
            (6, 'Divers'),
            (7, 'Verrerie'),
            (8, 'Produits Organiques'),
            (9, 'Produits Minéraux'),
            (10, 'Enzymes'),
            (11, 'Colorants'),
            (12, 'Entretien'),
            (13, 'Autres'),
            (14, 'Appareils de labo'),
            (15, 'Sécurité'),
            (16, 'Fournitures'),
            (17, 'Mobilier'),
            (18, 'Divers'),
            (19, 'Logiciels'),
            (20, 'DVD/VHS'),
            (21, 'Manuels Scolaires'),
            (22, 'Livres Scientifiques'),
            (23, 'Cartes/Posters'),
            (24, 'Divers'),
            (25, 'Générateurs'),
            (26, 'Mesures'),
            (27, 'Récepteurs'),
            (28, 'Connectique'),
            (29, 'Métaux'),
            (30, 'Divers')]

    rangement = StringField('Rangement', validators=[DataRequired()])
    commentaire = TextAreaField('Description' , validators=[DataRequired()])
    quantite = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=0)])
    unite = SelectField('Unité', choices=[None,'cm','g','ml'])
    complements = StringField('Compléments', validators=[DataRequired()])
    ficheFDS = FileField('Fiche De Sécurité', name='ficheFDS')
    seuil_quantite = IntegerField('Seuil de Quantité', validators=[NumberRange(min=0)])
    seuil_peremption = IntegerField('Seuil de Péremption (nb jours)', validators=[NumberRange(min=0)])
    categorie = SelectField('Catégorie', choices=lesC, validators=[DataRequired()])
    domaine = SelectField('Domaine', choices=lesD, validators=[DataRequired()])

class LostPasswordForm(FlaskForm):
    """ Formulaire de récupération du mot de passe. """    
    mail_field = EmailField('Adresse mail', validators=[DataRequired(), Email()])
