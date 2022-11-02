# -*- coding: utf-8 -*-
from flask import Flask, url_for, request, render_template, redirect
from fonction import *

# ------------------
# application Flask
# ------------------
app = Flask(__name__)


# ---------------------------------------
# les différentes pages (fonctions VUES)
# ---------------------------------------
# une page index avec des liens vers les différentes pages d'exemple d'utilisation de Flask
@app.route('/')
@app.route('/index')
def index():
    title = "index.LEGO"
    return render_template('index.html', title=title)


@app.route('/agiGREEN')
def agiGREEN():
    title = "AgiGreen"
    return render_template('page agiGREEN.html', title=title)


@app.route('/agiLEAN')
def agiLEAN():
    title = "AgiLean"
    return render_template('page agiLEAN.html', title=title)


@app.route('/agiLOG')
def agiLOG():
    title = "AgiLog"
    return render_template('page agiLOG.html', title=title)


@app.route('/agiPART')
def agiPART():
    title = "AgiPart"
    return render_template('page agiPART.html', title=title)


@app.route('/commandes')
def commandes():
    title = "Commande de kit"
    return render_template('page commande.html', title=title)


@app.route('/stock')
def stock():
    title = "Stock AgiLog"
    liste_stock = affichage_stock()
    liste_noms_entete = ["Désignation", "Code article", "Fournisseur", "Stock", "Seuil de commande"]
    liste_noms_case = ["designation", "code_article", "nom", "stock", "seuil_commande"]
    return render_template('page stock.html', title=title, liste_stock=liste_stock, liste_noms_entete=liste_noms_entete,
                           liste_noms_case=liste_noms_case)


# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
