Page a expedier

commande = SELECT id FROM commande_pieces

quand envoi:
UPDATE commande_pieces SET etat=envoye WHERE commande_pieces.id == commande

**
Page historique

SELECT id, date_validation, etat FROM commande_pieces

**
Page réception

commande = SELECT id FROM commande_pieces
UPDATE commande_pieces SET etat=valide WHERE commande_pieces.id == commande
UPDATE commande_pieces SET etat=invalide WHERE commande_pièces.id == commande

UPDATE commande_pièces SET date validation=date WHERE commande_pieces.id == commande

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

INSERT INTO contenu_commande_pieces SET etat=valide WHERE commande_pieces.id == commande
