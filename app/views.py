"""Toute les routes et les Formulaires"""
from flask import jsonify, render_template
from flask_login import login_required, login_user
from .app import app
from .models import Utilisateur

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
def admin_manage():
    user = Utilisateur.query.get(1)
    login_user(user)
    liste = Utilisateur.query.all()
    return render_template("gerer_utilisateurs.html", liste_users=liste)

@app.route("/get_user_info/<int:user_id>", methods=['GET'])
def get_user_info(user_id):
    user = Utilisateur.query.get(user_id)
    role_user = user.get_role()
    if user:
        user_info = {
            'id': user.id,
            'nom': user.nom,
            'prenom': user.prenom,
            'role': role_user.intitule,
            'password': user.password,
            'modifications': user.modifications
        }
        return jsonify(user_info)
    else:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
