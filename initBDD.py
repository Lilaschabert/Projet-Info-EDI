import sqlite3 as lite

#créer la connexion avec le fichier, et créer le fichier si il est inexistant
con = lite.connect('dev.db')

#récupération de la liste des Table dans listeTable
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master")
lignes = cur.fetchall()
listeTable=[elt[0] for elt in lignes]

print(listeTable)


if "fournisseur" not in listeTable:
	print("création de la table fournisseur")
	cur.execute("""CREATE TABLE fournisseur(
		id   INTEGER PRIMARY KEY AUTOINCREMENT ,
		nom  TEXT)""")

if "vehicule" not in listeTable:
	print("création de la table vehicule")
	cur.execute("""CREATE TABLE vehicule(
		id   INTEGER PRIMARY KEY AUTOINCREMENT ,
		nom  TEXT)""")

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
		FOREIGN KEY(idFournisseur) REFERENCES fournisseur(id))
		""")

if "kits" not in listeTable:
	print("création de la table kits")
	cur.execute("""CREATE TABLE kits(
		id   INTEGER PRIMARY KEY AUTOINCREMENT ,
		nom  TEXT)""")

if "commande_vehicule" not in listeTable:
	print("création de la table commande_vehicule")
	cur.execute("""CREATE TABLE commande_vehicule(
		id   INTEGER PRIMARY KEY AUTOINCREMENT ,
		id_vehicule      INTEGER UNSIGNED NOT NULL,
		date_commande    TIMESTAMP,
		date_validation  TIMESTAMP,
		etat             TEXT,
		FOREIGN KEY(id_vehicule) REFERENCES vehicule(id))""")

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

if "kit_dans_vehicule" not in listeTable:
	print("création de la table kit_dans_vehicule")
	cur.execute("""CREATE TABLE kit_dans_vehicule(
		id_kit       INTEGER UNSIGNED NOT NULL,
		id_vehicule  INTEGER UNSIGNED NOT NULL,
		nombre_kit   INT UNSIGNED NOT NULL,
		FOREIGN KEY(id_kit)      REFERENCES kits(id),
		FOREIGN KEY(id_vehicule) REFERENCES vehicule(id))""")

con.close()
