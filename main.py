# -*- coding: utf-8 -*-
from flask import Flask, url_for, request, render_template, redirect, flash
from fonction import *

# ------------------
# application Flask
# ------------------
app = Flask(__name__)
app.secret_key = 'the random string'


# ---------------------------------------
# les différentes pages (fonctions VUES)
# ---------------------------------------
# une page index avec des liens vers les différentes pages d'exemple d'utilisation de Flask
@app.route('/')
@app.route('/index')
def index():
    title = "index.LEGO"
    return render_template('index.html', title=title)


@app.route('/AgiGreen')
def agiGREEN():
    title = "AgiGreen"
    return render_template('page agiGREEN.html', title=title)


@app.route('/AgiLean')
def agiLEAN():
    title = "AgiLean"
    return render_template('page agiLEAN.html', title=title)


@app.route('/AgiLog')
def agiLOG():
    title = "AgiLog"
    return render_template('page agiLOG.html', title=title)


@app.route('/AgiPart')
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
    liste_entete = ["Désignation", "Code article"]
    liste_case = ["designation", "code_article"]
    liste_entete_input = ["Stock", "Seuil de commande", "Délai", "Niveau de recomplétion"]
    liste_case_input = ["stock", "seuil_commande", "delai", "niveau_recompletion"]
    if request.method == 'POST':
        liste_id = [piece["id"] for piece in liste_stock]
        dict_pieces = {}
        for id_piece in liste_id:
            dict_piececourante = {}
            for case_input in liste_case_input:
                value = request.form[str(id_piece) + "-" + case_input]
                if value == "None":
                    value = None
                elif case_input in ["stock", "seuil_commande", "niveau_recompletion"]:
                    try:
                        value = int(value)
                    except:
                        flash(case_input + " doit être un entier")
                        return redirect(url_for('init_stock'))
                dict_piececourante[case_input] = value
            dict_pieces[id_piece] = dict_piececourante
        try:
            sql_init_stock(dict_pieces)
            flash("Stock initiés!")
        except:
            flash("Problème d'initialisation")
        return redirect(url_for('init_stock'))
    return render_template('page initialisation stock.html', title=title, liste_stock=liste_stock,
                           liste_entete=liste_entete,
                           liste_case=liste_case, liste_entete_input=liste_entete_input,
                           liste_case_input=liste_case_input)


@app.route('/commande_pieces', methods=['GET', 'POST'])
def commande_pieces():
    """Affiche toutes les pièces dont le stock fictif (stock réel+stock en commande) est en dessus du seuil de commande
    La case de la quantité à commander est prérempli avec le delta entre le stock fictif et le niveau de recompletion
    On peut générer la page pour commander toutes les pièces (ou partie en mettant 'None' pour les pièces que l'on ne veut pas commander)
    en rajoutant ?forcer=True à la fin de l'URL"""
    title = "Commande de pièces par AgiLog"

    liste_entete = ["Désignation", "Code article", "Fournisseur", "Stock", "Stock fictif", "Seuil de commande",
                    "Niveau de recomplétion"]
    liste_case = ["designation", "code_article", "nom", "stock", "stock_fictif", "seuil_commande",
                  "niveau_recompletion"]
    liste_entete_input = ["Quantité à commander"]
    liste_case_input = ["commande_default"]

    filtre = True
    if request.method == 'GET':
        forcer = request.args.get("forcer")
        if forcer == "True":
            filtre = False
    liste_stock = affichage_stock_commande(filtre=filtre)
    if request.method == 'POST':
        liste_code_article = [piece["code_article"] for piece in liste_stock]
        dict_pieces = {}
        for code_article in liste_code_article:
            value = request.form[str(code_article)]
            if value != "None":
                try:
                    value = int(value)
                except:
                    flash("La quantité à commander doit être un entier (ou 'None')")
                    return redirect(url_for('commande_pieces'))
                dict_pieces[code_article] = value
        date_commande = request.form["date"]
        try:
            passer_commande_pieces(dict_pieces, date_commande)
            flash("Commande(s) envoyée(s)!")
        except:
            flash("Problème lors de la commande")
        return redirect(url_for('commande_pieces'))
    return render_template('page commande pieces.html', title=title, liste_stock=liste_stock, liste_entete=liste_entete,
                           liste_case=liste_case, liste_entete_input=liste_entete_input,
                           liste_case_input=liste_case_input, filtre=filtre)


@app.route('/<string:entite>/historique-commandes')
def historique(entite):
    if entite == "AgiLog":
        nom_fournisseur = ""
    else:
        nom_fournisseur = entite
    title = "Historique " + entite
    liste_commandes = historique_commande_pieces(nom_fournisseur=nom_fournisseur)
    liste_noms_entete = ["id", "Fournisseur", "Etat", "Date de commande", "Date de validation"]
    liste_noms_case = ["id", "nom", "etat", "date_commande", "date_validation"]
    return render_template('page historique commande.html', title=title, liste_commandes=liste_commandes,
                           liste_noms_entete=liste_noms_entete,
                           liste_noms_case=liste_noms_case, entite=entite)


@app.route('/<string:entite>/commande/<int:id_cmd>', methods=['GET', 'POST'])
def detail_commande(entite, id_cmd):
    if request.method == 'POST':
        if entite in ["AgiLog","AgiPart","AgiGreen","admin"]:
            etat = request.form["etat"]
            if etat == "Valider":
                etat = "validee"
            elif etat == "Invalider":
                etat = "invalidee"
            elif etat != "Envoyer":
                flash("Etat incorect")
                return redirect(url_for('detail_commande', entite=entite, id_cmd=id_cmd))

            if etat in ["validee","invalidee"]:
                date_validation = request.form["date"]
                resultat = change_etat_commande_recu(id_cmd, etat, date_validation)
            else:
                resultat = expedition_commande(id_cmd)

            if resultat:
                flash("Etat confirmé!")
                return redirect(url_for('detail_commande', entite=entite, id_cmd=id_cmd))
            else:
                flash("Erreur dans la modification de l'état")
                return redirect(url_for('detail_commande', entite=entite, id_cmd=id_cmd))

    title = "Commande " + str(id_cmd)
    donnee_cmd, liste_pieces = sql_detail_commande_pieces(id_cmd)
    liste_noms_entete = ["Désignation", "Code article", "Nombre de pièces"]
    liste_noms_case = ["designation", "code_article", "nombre_piece"]
    dict_donnee = {
        "date_commande": "Date de commande",
        "date_validation": "Date de reception",
        "etat": "Etat",
        "nom": "Fournisseur"
    }
    return render_template('page detail commande.html', title=title, entite=entite,
                           liste_pieces=liste_pieces, liste_noms_entete=liste_noms_entete,
                           liste_noms_case=liste_noms_case,
                           donnee_cmd=donnee_cmd, dict_donnee=dict_donnee)


@app.route('/AgiLean/creation_kit', methods=['GET', 'POST'])
def creation_kit():
    title = "Création d'un kit"

    liste_entete = ["Désignation", "Code article"]
    liste_case = ["designation", "code_article"]
    liste_entete_input = ["Quantité"]

    liste_pieces = sql_pieces_existantes()
    if request.method == 'POST':
        liste_code_article = [piece["code_article"] for piece in liste_stock]
        dict_pieces = {}
        for code_article in liste_code_article:
            value = request.form[str(code_article)]
            if value != "None":
                try:
                    value = int(value)
                except:
                    flash("La quantité à commander doit être un entier (ou 'None')")
                    return redirect(url_for('commande_pieces'))
                dict_pieces[code_article] = value
        date_commande = request.form["date"]
        try:
            passer_commande_pieces(dict_pieces, date_commande)
            flash("Commande(s) envoyée(s)!")
        except:
            flash("Problème lors de la commande")
        return redirect(url_for('commande_pieces'))
    return render_template('page creation kit.html', title=title, liste_pieces=liste_pieces, liste_entete=liste_entete,
                           liste_case=liste_case, liste_entete_input=liste_entete_input)


@app.route('/AgiLean/kit/<int:id_kit>', methods=['GET', 'POST'])
def detail_kit(id_kit):
    donnee_kit, liste_pieces = sql_detail_kit(id_kit)
    title = str(donnee_kit["nom"])
    liste_noms_entete = ["Désignation", "Code article", "Nombre de pièces"]
    liste_noms_case = ["designation", "code_article", "nombre_piece"]
    return render_template('page detail kit.html', title=title,
                           liste_pieces=liste_pieces, liste_noms_entete=liste_noms_entete,
                           liste_noms_case=liste_noms_case, donnee_kit=donnee_kit)


# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
