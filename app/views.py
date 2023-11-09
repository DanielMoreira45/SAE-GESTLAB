"""Toute les routes et les Formulaires"""
from flask import jsonify, render_template, url_for, redirect, url_for, redirect
from flask_login import login_required, login_user
from .app import app, db
from .models import Utilisateur, Role
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    id = HiddenField('id')
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    id_role = SelectField('role', validators=[DataRequired()], choices=[(1, 'Administrateur'), (2, 'Professeur'), (3, 'Etablissement')])
    modifications = RadioField('modifications', validators=[DataRequired()])

@app.route('/login/')
def login():
    return None #TODO

@app.route('/logout/')
def logout():
    return None #TODO

@app.route('/a/')
def admin_add():
    return None #TODO

@app.route('/b/')
def consult():
    return None #TODO

@app.route('/c/')
def delivery():
    return None #TODO

@app.route('/d/')
def new_commande():
    return None #TODO

@app.route("/admin/manage/")
# @login_required
def admin_manage(user_id=1):
    user = Utilisateur.query.get(user_id)
    login_user(user)
    liste = Utilisateur.query.all()
    roles = Role.query.all()
    return render_template("gerer_utilisateurs.html",
                           liste_users=liste,
                           roles=roles,
                           current_user_selected=user)

@app.route("/get_user_info/<int:user_id>", methods=['GET'])
def get_user_info(user_id):
    user = Utilisateur.query.get(user_id)
    role_user = user.get_role()
    if user:
        user_info = {
            'id': user.id,
            'nom': user.nom,
            'prenom': user.prenom,
            'id_role': user.id_role,
            'role_name': role_user.intitule,
            'password': user.password,
            'modifications': user.modifications
        }
        return jsonify(user_info)
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

@app.route('/update_user/', methods=['POST'])
def update_user():
    les_roles = {'Administrateur': 1, 'Professeur': 2, 'Etablissement': 3}
    f = UserForm()
    user_modified = Utilisateur.query.get(f.id.data)
    user_modified.nom = f.nom.data
    user_modified.prenom = f.prenom.data
    user_modified.password = f.password.data
    if f.id_role.data in les_roles:
        user_modified.id_role = les_roles[f.id_role.data]
    user_modified.modifications = eval(f.modifications.data)
    db.session.commit()
    return redirect(url_for('admin_manage'))
