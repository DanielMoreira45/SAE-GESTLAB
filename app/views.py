"""Toute les routes et les Formulaires"""

from .app import app
from flask import render_template, url_for, redirect, request

@app.route("/")
def home():
    return render_template("home.html")