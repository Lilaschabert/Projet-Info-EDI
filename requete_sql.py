import sqlite3 as lite


def connection_bdd():
    """connection au fichier bdd"""
    con = lite.connect('dev.db')
    con.row_factory = lite.Row
    return con


# page historique
def historique_commande(nom_fournisseur=""):
    """requetes pour les pages d'historique des commandes"""
    conn = connection_bdd()
    cur = conn.cursor()
    querry = """SELECT id,date_commande,date_validation,etat FROM commande_pieces"""
    if nom_fournisseur != "":
        querry += "JOIN fournisseur ON fournisseur.id=commande_pieces.idFournisseur WHERE fournisseur.nom=" + nom_fournisseur
    cur.execute(querry + ";")
    lignes = cur.fetchall()
    conn.close()
    return lignes


# page commandes à expedier
def commande_a_expedier(nom_fournisseur):
    """requetes pour récupérer les commandes à expedier d'un fournisseur donné"""
    conn = connection_bdd()
    cur = conn.cursor()
    querry = """SELECT commande_pieces.id FROM commande_pieces
    JOIN fournisseur ON fournisseur.id=commande_pieces.idFournisseur
    WHERE fournisseur.nom=? AND etat='commandee'
    """
    cur.execute(querry, (nom_fournisseur,))
    lignes = cur.fetchall()
    conn.close()
    return lignes


def expedition_commande(id_commande):
    """requete pour valider l'expedition d'une commande"""
    try:
        conn = connection_bdd()
        cur = conn.cursor()
        cur.execute("UPDATE commande_pieces SET etat='envoyee' WHERE id = ?", (str(id_commande)))
        conn.commit()
        conn.close()
        return True
    except lite.Error:
        return False


# page validations des receptions de commandes
def commandes_pieces_recu():
    """requete pour renvoyer la listes des commandes reçu par AgiLog, non encore validée/invalidée"""
    conn = connection_bdd()
    cur = conn.cursor()
    querry = """SELECT id FROM commande_pieces
    WHERE etat='envoyee';"""
    cur.execute(querry)
    lignes = cur.fetchall()
    conn.close()
    return lignes


def liste_pieces_commande(id_commande):
    """requete pour renvoyer les pièces d'une commandes définie par son id"""
    conn = connection_bdd()
    cur = conn.cursor()
    querry = """SELECT designation,code_article,nombre_piece FROM pieces
    JOIN contenu_commande_pieces ON id_piece=pieces.id
    JOIN commande_pieces ON commande_pieces.id=id_commande
    WHERE commande_pieces.id=?;"""
    cur.execute(querry, (str(id_commande)))
    lignes = cur.fetchall()
    conn.close()
    return lignes


def change_etat_commande_recu(id_commande, etat, date_validation):
    """requete pour valider/invalider une commande reçu par AgiLog"""
    if not (etat in ["validee", "invalidee"]):
        return ("etat incorrect")
    try:
        conn = connection_bdd()
        cur = conn.cursor()
        cur.execute("UPDATE commande_pieces SET etat=?,date_validation=? WHERE id = ?",
                    (etat, date_validation, str(id_commande)))
        conn.commit()
        conn.close()
        return True
    except lite.Error:
        return False


def passer_commande(dict_nombre_pieces, date_commande):
    """<dict_nombre_pieces> est un dictionnaire avec pour clé le code_article des pièces à commander,
    et comme valeur dans chaque case le nombre de pièces correspondant"""
    conn = connection_bdd()
    cur = conn.cursor()
    cur.execute("SELECT id FROM fournisseur;")
    liste_id_fournisseur = cur.fetchall()
    dict_commande_par_fournisseur = {}
    for fournisseur in liste_id_fournisseur:
        dict_commande_par_fournisseur[fournisseur['id']] = {}

    cur.execute("SELECT id,code_article,idFournisseur FROM pieces;")
    liste_pieces = cur.fetchall()
    dict_idfournisseur_pieces = {}
    dict_id_pieces = {}
    for piece in liste_pieces:
        dict_id_pieces[piece['code_article']] = piece['id']
        dict_idfournisseur_pieces[piece['code_article']] = piece['idFournisseur']

    for code_article, nombre_pieces in dict_nombre_pieces.items():
        dict_commande_par_fournisseur[dict_idfournisseur_pieces[code_article]][
            dict_id_pieces[code_article]] = nombre_pieces

    for fournisseur in liste_id_fournisseur:
        if len(dict_commande_par_fournisseur[fournisseur['id']]) >= 1:
            cur.execute("INSERT INTO commande_pieces('date_commande', 'etat', 'idFournisseur') VALUES (?,?,?);",
                        (date_commande, "commandee", fournisseur['id']))
            conn.commit()
            # cur.execute("SELECT id FROM commande_pieces WHERE date_commande=? AND etat=? AND idFournisseur=?;",(date_commande, "commandee", fournisseur['id']))
            # id_commande = cur.fetchall()[0]['id']
            cur.execute("SELECT SEQ FROM SQLITE_SEQUENCE WHERE NAME='commande_pieces';")
            id_commande = cur.fetchall()[0]['SEQ']
            for id_pieces, nombre_pieces in dict_commande_par_fournisseur[fournisseur['id']].items():
                cur.execute("INSERT INTO contenu_commande_pieces('id_piece', 'id_commande', 'nombre_piece') VALUES (?,?,?)",
                            (str(id_pieces), str(id_commande), str(nombre_pieces)))
            conn.commit()
    conn.close()
    return True



"""
## AGILOG

LIEN AVEC AGIGREEN/PARTS

**
Page stock initiaux

reference = SELECT id FROM pieces

UPDATE pieces SET stock=? WHERE pieces.id == ? / stock_init,reference
UPDATE pieces SET seuil_commande cmd=? WHERE pieces.id == ? / seuil,reference
UPDATE pieces SET delai cmd=? WHERE pieces.id == ? / delai,reference
UPDATE pieces SET niveau_recompletion=? WHERE pieces.id == ? / stock_CQ,reference

**
Page consultation stock

SELECT id, stock FROM pieces


LIEN AVEC AGILEAN

**
Page a expedier

commande = SELECT id FROM commande_kits

quand envoi:
UPDATE commande_kits SET etat=envoye WHERE commande_kits.id == commande






## AGILEAN ##

**
Page passer commande

SELECT nom FROM kits
"INSERT INTO contenu_commande_kit('id_kit','id_commande','nombre_kit') VALUES (?,?,?)" (id_kit,id_commande,nombre_kit)
"INSERT INTO commande_kit('id','date_commande','date_validation','etat') VALUES (?,?,?,?)" (id,date_commande,NONE,'en cours')

**
Page reception

commande = SELECT id FROM commande_kits
UPDATE commande_kits SET etat=valide WHERE commande_kits.id == commande
UPDATE commande_kits SET etat=invalide WHERE commande_kits.id == commande

UPDATE commande_kits SET date_validation=date WHERE commande_kits.id == commande



# commande={"B2*2":1,"JT":3,"P1*2":2,"P4*4":2,"P1*1":1}
# passer_commande(commande, "test")
"""