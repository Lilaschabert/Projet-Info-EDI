import sqlite3 as lite


def connection_bdd():
    """connection au fichier bdd"""
    con = lite.connect('dev.db')
    con.row_factory = lite.Row
    return con


# page historique
def historique_commande(nomFournisseur=""):
    """requetes pour les pages d'historique des commandes"""
    conn = connection_bdd()
    cur = conn.cursor()
    querry = """SELECT id,date_commande,date_validation,etat FROM commande_pieces"""
    if nomFournisseur != "":
        querry += "JOIN fournisseur ON fournisseur.id=commande_pieces.idFournisseur WHERE fournisseur.nom=" + nomFournisseur
    cur.execute(querry + ";")
    lignes = cur.fetchall()
    conn.close()
    return lignes


##page commandes à expedier
def commande_a_expedier(nomFournisseur):
    """requetes pour récupérer les commandes à expedier d'un fournisseur donné"""
    conn = connection_bdd()
    cur = conn.cursor()
    querry = """SELECT id FROM commande_pieces
    JOIN fournisseur ON fournisseur.id=commande_pieces.idFournisseur
    WHERE fournisseur.nom=? AND etat='commandee'
    """
    cur.execute(querry, (nomFournisseur))
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


##page validations des receptions de commandes
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
    WHERE pieces.id=?;"""
    cur.execute(querry,(str(id_commande)))
    lignes = cur.fetchall()
    conn.close()
    return lignes

def change_etat_commande_recu(id_commande,etat,date_validation):
    """requete pour valider/invalider une commande reçu par AgiLog"""
    if not(etat in ["validee","invalidee"]):
        return("etat incorrect")
    try:
        conn = connection_bdd()
        cur = conn.cursor()
        cur.execute("UPDATE commande_pieces SET etat='?',date_validation='?' WHERE id = ?", (etat,date_validation,str(id_commande)))
        conn.commit()
        conn.close()
        return True
    except lite.Error:
        return False






"""
def template_lecture(lettre):
    conn = connection_bdd()
    cur = conn.cursor()
    cur.execute("SELECT nom, prenom, role FROM personnes WHERE prenom LIKE ?", (lettre + "%",))
    lignes = cur.fetchall()
    conn.close()
    return lignes

# connecte à la BDD et insère une nouvelle ligne avec les valeurs données
def template_insertion(nom, prenom, role):
    try:
        conn = connection_bdd()
        cur = conn.cursor()
        cur.execute("INSERT INTO personnes('nom', 'prenom', 'role') VALUES (?,?,?)", (nom, prenom, role))
        conn.commit()
        conn.close()
        return True
    except lite.Error:
        return False
"""

"""
## AGILOG

LIEN AVEC AGIGREEN/PARTS

**
Page réception

commande = SELECT id FROM commande_pieces
UPDATE commande_pieces SET etat=valide WHERE commande_pieces.id == commande
UPDATE commande_pieces SET etat=invalide WHERE commande_pieces.id == commande

UPDATE commande_pièces SET date_validation=date WHERE commande_pieces.id == commande

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

**
Page passer commande

SELECT id, stock, seuil_commande, delai, niveau_recompletion FROM pieces

"INSERT INTO contenu_commande_pieces('id_piece','id_commande','nombre_piece') VALUES (?,?,?)" (id_piece,id_commande,nombre_piece)
"INSERT INTO commande_pieces('id','date_commande','date_validation','etat','idFournisseur') VALUES (?,?,?,?,?)" (id,date_commande,NONE,'en cours',idFournisseur)



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
"""
test=liste_pieces_commande(1)
print(test)