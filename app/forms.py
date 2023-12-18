from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class MaterielModificationForm(FlaskForm):
    """Formulaire de modification du matériel."""

    nom = StringField('Nom', validators=[DataRequired()])
    domaine = StringField('Domaine', validators=[DataRequired()])
    categorie = StringField('Catégorie', validators=[DataRequired()])
    reference = StringField('Référence', validators=[DataRequired()])
    
    quantiteRes = IntegerField('Quantité restante')
    quantiteTot = IntegerField('Quantité totale', validators=[DataRequired()])

    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Modifier')

    def __init__(self, materiel=None, *args, **kwargs):
        super(MaterielModificationForm, self).__init__(*args, **kwargs)
        
        # Définir les valeurs par défaut en fonction de l'instance 'materiel' fournie
        if materiel:
            self.nom.default = materiel.nom
            self.domaine.default = materiel.domaine.nom
            self.categorie.default = materiel.categorie.nom
            self.reference.default = materiel.reference
            self.quantiteRes.default = materiel.quantite_restante
            self.quantiteTot.default = materiel.quantite_globale
            self.description.default = materiel.complements

        self.process()
