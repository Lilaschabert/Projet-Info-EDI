
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
		id   SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
		nom  TEXT)""")

if "vehicule" not in listeTable:
	print("création de la table vehicule")
	cur.execute("""CREATE TABLE vehicule(
		id   SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
		nom  TEXT)""")

if "pieces" not in listeTable:
	print("création de la table pieces")
	cur.execute("""CREATE TABLE pieces(
		id SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
		designation         TEXT,
		code_article        TEXT,
		idFournisseur       SMALLINT UNSIGNED,
		stock               INT,
		seuil_commande      INT UNSIGNED,
		delai               INT UNSIGNED,
		niveau_recompletion INT UNSIGNED)""")

if "kits" not in listeTable:
	print("création de la table kits")
	cur.execute("""CREATE TABLE kits(
		id   SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
		nom  TEXT)""")

if "commande_vehicule" not in listeTable:
	print("création de la table commande_vehicule")
	cur.execute("""CREATE TABLE commande_vehicule(
		id  SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
		id_vehicule      SMALLINT UNSIGNED NOT NULL,
		date_commande    TIMESTAMP,
		date_validation  TIMESTAMP,
		etat             TEXT)""")

if "commande_kits" not in listeTable:
	print("création de la table commande_kits")
	cur.execute("""CREATE TABLE commande_kits(
		id  SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
		date_commande    TIMESTAMP,
		date_validation  TIMESTAMP,
		etat             TEXT)""")

if "commande_pieces" not in listeTable:
	print("création de la table commande_pieces")
	cur.execute("""CREATE TABLE commande_pieces(
		id  SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
		date_commande    TIMESTAMP,
		date_validation  TIMESTAMP,
		etat             TEXT,
		idFournisseur    SMALLINT UNSIGNED)""")
		
		

if "piece_kit" not in listeTable:
	print("création de la table piece_kit")	
	cur.execute("""CREATE TABLE piece_kit(
		id_piece      SMALLINT UNSIGNED NOT NULL,
		id_kit        SMALLINT UNSIGNED NOT NULL,
		nombre_piece  INT UNSIGNED NOT NULL)""")

if "contenu_commande_kit" not in listeTable:
	print("création de la table commande_kits")
	cur.execute("""CREATE TABLE contenu_commande_kit(
		id_kit       SMALLINT UNSIGNED NOT NULL,
		id_commande  SMALLINT UNSIGNED NOT NULL,
		nombre_kit   INT UNSIGNED NOT NULL)""")

if "contenu_commande_pieces" not in listeTable:
	print("création de la table contenu_commande_pieces")
	cur.execute("""CREATE TABLE contenu_commande_pieces(
		id_piece      SMALLINT UNSIGNED NOT NULL,
		id_commande   SMALLINT UNSIGNED NOT NULL,
		nombre_piece  INT UNSIGNED NOT NULL)""")

if "kit_dans_vehicule" not in listeTable:
	print("création de la table kit_dans_vehicule")
	cur.execute("""CREATE TABLE kit_dans_vehicule(
		id_kit       SMALLINT UNSIGNED NOT NULL,
		id_vehicule  SMALLINT UNSIGNED NOT NULL,
		nombre_kit   INT UNSIGNED NOT NULL)""")

con.close()
