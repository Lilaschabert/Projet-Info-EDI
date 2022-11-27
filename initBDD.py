import sqlite3 as lite


def connection():
    # créer la connexion avec le fichie et créer le fichier s'il est inexistant
    con = lite.connect('dev.db')
    cur = con.cursor()
    return (con, cur)


def creationFournisseur():
    con, cur = connection()
    liste_nom = ["AgiGreen", "AgiPart"]
    for nom in liste_nom:
        cur.execute("INSERT INTO fournisseur(nom) VALUES (?);", (nom,))
    con.commit()
    con.close()


def creationPiece():
    con, cur = connection()
    listePiece = [
        ["Brique 2*2", "B2*2", "AgiGreen"],
        ["Moyeu", "MY", "AgiGreen"],
        ["Jante", "JT", "AgiGreen"],
        ["Pneu", "PN", "AgiGreen"],
        ["Plaque lisse 2*2", "PL2*2", "AgiGreen"],
        ["Plaque 2*4", "P2*4", "AgiGreen"],
        ["Plaque 1*2", "P1*2", "AgiGreen"],
        ["Grille", "GR", "AgiGreen"],
        ["Renvoi d'angle", "RA", "AgiGreen"],
        ["Feux avant", "FV", "AgiGreen"],
        ["Plaque 1*4", "P1*4", "AgiGreen"],
        ["Feux arrière", "FR", "AgiGreen"],
        ["Châssis Garde boue", "GB", "AgiGreen"],
        ["Plaque 2*4", "P2*4", "AgiGreen"],
        ["Plaque 1*4", "P1*4", "AgiGreen"],
        ["M Plaque 1*3", "P1*3", "AgiGreen"],
        ["M Plaque 1*3", "P1*3", "AgiGreen"],
        ["Plaque 4*4", "P4*4", "AgiPart"],
        ["Plaque 2*12", "P2*12", "AgiGreen"],
        ["Plaque 2*8", "P2*8", "AgiGreen"],
        ["Habitacle Pare-brise", "PB", "AgiGreen"],
        ["Attache", "AT", "AgiGreen"],
        ["Volant", "VL", "AgiGreen"],
        ["Siège", "SG", "AgiGreen"],
        ["Fenêtre", "FN", "AgiGreen"],
        ["Plaque 4*4", "P4*4", "AgiPart"],
        ["M Plaque 1*4", "P1*4", "AgiGreen"],
        ["M Plaque 1*4", "P1*4", "AgiGreen"],
        ["Plaque 1*6", "P1*6", "AgiGreen"],
        ["Arceau", "AC", "AgiPart"],
        ["Plaque 1*1", "P1*1", "AgiGreen"],
        ["Plaque 1*6", "P1*6", "AgiGreen"],
        ["Plaque 1*4", "P1*4", "AgiGreen"],
        ["Equerre", "EQ", "AgiPart"],
        ["Toit", "TT", "AgiPart"],
        ["Brique 2*4", "B2*4", "AgiGreen"],
        ["Brique 1*4", "B1*4", "AgiGreen"]]
    for piece in listePiece:
        designation, code_article, fournisseur = piece
        cur.execute("SELECT id FROM fournisseur WHERE nom=?", (fournisseur,))
        idFournisseur = cur.fetchone()[0]
        cur.execute("INSERT INTO pieces(designation,code_article,idFournisseur) VALUES (?,?,?);",
                    (designation, code_article, idFournisseur))
    con.commit()
    con.close()


def main():
    con, cur = connection()
    # récupération de la liste des Tables dans listeTable
    cur.execute("SELECT name FROM sqlite_master")
    lignes = cur.fetchall()
    listeTable = [elt[0] for elt in lignes]

    if "fournisseur" not in listeTable:
        print("création de la table fournisseur")
        cur.execute("""CREATE TABLE fournisseur(
            id   INTEGER PRIMARY KEY AUTOINCREMENT ,
            nom  TEXT)""")
        creationFournisseur()

    if "pieces" not in listeTable:
        print("création de la table pieces")
        cur.execute("""CREATE TABLE pieces(
            id   INTEGER PRIMARY KEY AUTOINCREMENT ,
            designation         TEXT NOT NULL,
            code_article        TEXT NOT NULL,
            idFournisseur       INTEGER UNSIGNED NOT NULL,
            stock               INT DEFAULT 0,
            seuil_commande      INT UNSIGNED,
            delai               INT UNSIGNED,
            niveau_recompletion INT UNSIGNED,
            FOREIGN KEY(idFournisseur) REFERENCES fournisseur(id))""")
        creationPiece()

    if "kits" not in listeTable:
        print("création de la table kits")
        cur.execute("""CREATE TABLE kits(
            id   INTEGER PRIMARY KEY AUTOINCREMENT ,
            nom  TEXT)""")

    if "commande_kits" not in listeTable:
        print("création de la table commande_kits")
        cur.execute("""CREATE TABLE commande_kits(
            id   INTEGER PRIMARY KEY AUTOINCREMENT ,
            date_commande    TIMESTAMP,
            date_validation  TIMESTAMP,
            etat             TEXT)""")

    if "commande_pieces" not in listeTable:
        print("création de la table commande_pieces")
        cur.execute("""CREATE TABLE commande_pieces(
            id   INTEGER PRIMARY KEY AUTOINCREMENT ,
            date_commande    TIMESTAMP,
            date_validation  TIMESTAMP,
            etat             TEXT,
            idFournisseur    INTEGER UNSIGNED NOT NULL,
            FOREIGN KEY(idFournisseur) REFERENCES fournisseur(id))""")

    if "piece_kit" not in listeTable:
        print("création de la table piece_kit")
        cur.execute("""CREATE TABLE piece_kit(
            id_piece      INTEGER UNSIGNED NOT NULL,
            id_kit        INTEGER UNSIGNED NOT NULL,
            nombre_piece  INT UNSIGNED NOT NULL,
            FOREIGN KEY(id_piece) REFERENCES pieces(id),
            FOREIGN KEY(id_kit)   REFERENCES kits(id))""")

    if "contenu_commande_kit" not in listeTable:
        print("création de la table commande_kits")
        cur.execute("""CREATE TABLE contenu_commande_kit(
            id_kit       INTEGER UNSIGNED NOT NULL,
            id_commande  INTEGER UNSIGNED NOT NULL,
            nombre_kit   INT UNSIGNED NOT NULL,
            FOREIGN KEY(id_kit)      REFERENCES kits(id),
            FOREIGN KEY(id_commande) REFERENCES commande_kits(id))""")

    if "contenu_commande_pieces" not in listeTable:
        print("création de la table contenu_commande_pieces")
        cur.execute("""CREATE TABLE contenu_commande_pieces(
            id_piece      INTEGER UNSIGNED NOT NULL,
            id_commande   INTEGER UNSIGNED NOT NULL,
            nombre_piece  INT UNSIGNED NOT NULL,
            FOREIGN KEY(id_piece)    REFERENCES pieces(id),
            FOREIGN KEY(id_commande) REFERENCES commande_pieces(id))""")

    con.close()


main()
