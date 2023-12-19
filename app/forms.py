"Formulaires de l'application"

from flask_wtf import FlaskForm
from wtforms import FileField, StringField, HiddenField, PasswordField, SelectField, RadioField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from .models import Utilisateur

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
    ficheFDS = FileField('Fiche De Sécurité')
    seuil_quantite = IntegerField('Seuil de Quantité', validators=[NumberRange(min=0)])
    seuil_peremption = IntegerField('Seuil de Péremption (nb jours)', validators=[NumberRange(min=0)])
    categorie = SelectField('Catégorie', choices=lesC, validators=[DataRequired()])
    domaine = SelectField('Domaine', choices=lesD, validators=[DataRequired()])