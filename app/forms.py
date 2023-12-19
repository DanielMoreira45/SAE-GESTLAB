from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, IntegerField
from wtforms.validators import DataRequired

from app.models import Domaine

class MaterielModificationForm(FlaskForm):
    """Formulaire de modification du matériel."""

    nom = StringField('Nom', validators=[DataRequired()])
    domaine = SelectField('Domaine', validators=[DataRequired()])
    categorie = SelectField('Catégorie', validators=[DataRequired()])
    reference = StringField('Référence', validators=[DataRequired()])
    hiddenref = HiddenField('hiddenref')
    
    quantiteRes = IntegerField('Quantité restante')
    quantiteTot = IntegerField('Quantité totale', validators=[DataRequired()])
    quantiteMax = IntegerField('Quantité maximale', validators=[DataRequired()])

    description = StringField('Description', validators=[DataRequired()])

    def __init__(self, materiel=None, *args, **kwargs):
        super(MaterielModificationForm, self).__init__(*args, **kwargs)
        
        # Définir les valeurs par défaut en fonction de l'instance 'materiel' fournie
        if materiel:
            self.nom.default = materiel.nom
            self.reference.default = materiel.reference
            self.quantiteRes.default = materiel.quantite_restante
            self.quantiteTot.default = materiel.quantite_globale
            self.description.default = materiel.complements
            self.hiddenref.default = materiel.reference
            self.quantiteMax.default = materiel.quantite_max
            self.categorie.default = materiel.categorie.code
            self.domaine.default = materiel.domaine.code

        self.process()

    def set_domaine_choices(self, choices):
        self.domaine.choices = choices

    def set_categorie_choices(self, choices):
        self.categorie.choices = choices

    def get_domaine(self):
        return self.domaine.data
