"""Toute les routes et les Formulaires"""
from flask import render_template
from flask_login import login_required
from .app import app
from .models import Utilisateur

# @app.route("/")

@app.route("/admin/manage/")
# @login_required
def admin_manage():
    liste = Utilisateur.query.all()
    return render_template("gerer_utilisateurs.html", liste_users=liste)
