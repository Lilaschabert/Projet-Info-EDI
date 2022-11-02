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


@app.route('/init_stock', methods=['GET', 'POST'])
def init_stock():
    title = "Initialisation Stock AgiLog"
    liste_stock = affichage_stock()
    liste_entete = ["Désignation","Code article"]
    liste_case   = ["designation","code_article"]
    liste_entete_input = ["Stock","Seuil de commande","Délai","Niveau de recomplétion"]
    liste_case_input   = ["stock","seuil_commande",  "delai","niveau_recompletion"]
    if request.method == 'POST':
        liste_id=[piece["id"] for piece in liste_stock]
        dict_pieces={}
        for id_piece in liste_id:
            dict_piececourante={}
            for case_input in liste_case_input:
                value=request.form[str(id_piece)+"-"+case_input]
                if value=="None":
                    value=None
                if case_input == "stock":
                    value=int(value)
                dict_piececourante[case_input]=value
            dict_pieces[id_piece]=dict_piececourante
        print(dict_pieces)
    """
        # la quantité peut être flottante, et négative (pour corriger un stock par exemple, si on veut transférer des stock d'un pian's vers un autre)
        quantite = request.form["quantite"]
        try:
            quantite = float(quantite)
        except:
            flash("la quantité doit être un nombre!")
            return redirect(url_for('init_stock'))

        # l'idComptoir est la clé primaire de la base stock, cela doit doc être un entier stricetement positif
        idComptoir = request.form["id"]
        try:
            idComptoir = int(idComptoir)
        except:
            flash("l'idComptoir est erroné (non entier)!")
            return redirect(url_for('init_stock'))
        if idComptoir <= 0:
            flash("l'idComptoir est erroné (<=0)!")
            return redirect(url_for('init_stock'))

        # on essaye de recupérer la ligne dans la table 'stock' qui correspond à l'id, et on vérifie si elle existe
        stocks = Stock.query.filter_by(id=idComptoir).first()
        if type(stocks) == type(None):
            flash("Comptoir inexistant!")
            return redirect(url_for('init_stock'))

        # les données communes aux deux forms sont récupéré, on différencie maintenant les 2 form
        if form_name == "corr":
            stocks.stock = stocks.stock + quantite
            db.session.commit()
            flash("correction ok")
            return redirect(url_for('init_stock'))

        if form_name == "appro":
            # on essaye de recupérer la ligne dans la table 'Comptoir' qui a pour nom 'reserve'. Ceci permet d'accéder essuite à son stock avec son id.
            # ainsi, ce n'est pas l'id de la reserve dans la table stock qui est fixe, mais le nom du comptoir reserve.
            comptoirReserve = Comptoir.query.filter_by(name="reserve").first()
            if type(comptoirReserve) == type(None):
                flash("Reserve inexistant!")
                return redirect(url_for('commande'))

            # même si le comptoir reserve existe, le stock de matière première dont on cherche à faire l'approvisionnement n'est pas nécessairement créer
            reserve = Stock.query.filter_by(comptoir_id=comptoirReserve.id,
                                            matierepremiere_id=stocks.matierepremiere_id).first()
            if type(reserve) == type(None):
                flash("Pas de reserve de ce stock!")
                return redirect(url_for('init_stock'))
            if reserve.stock < quantite:
                flash("Pas assez de matiere en stock!")
                return redirect(url_for('init_stock'))

            # ici, on enlève seulement la quantité de matière de la reserve.
            # la matière sera ajouté dans le stock du pians quand il y aura confirmation de l'arrivé de l'appro à travers la page commande
            reserve.stock = reserve.stock - quantite
            db.session.commit()
            ajoutCommande(stocks.id, quantite)
            flash("appro lancée!")
            return redirect(url_for('init_stock'))"""
    return render_template('page initialisation stock.html', title=title, liste_stock=liste_stock, liste_entete=liste_entete,
                           liste_case=liste_case,liste_entete_input=liste_entete_input,liste_case_input=liste_case_input)


# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------
if __name__ == '__main__':
    app.run(debug=True)