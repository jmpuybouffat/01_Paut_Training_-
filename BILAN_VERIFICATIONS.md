# Bilan de vérification — GUIDE TESTS

Révision de l’application au 2 novembre 2026. Vérifications logicielles automatisées, sans essai sur un instrument UT ni sur le PC de l’évaluateur.

## Résultats

- 20 tests Python/Streamlit réussis : géométrie, planification, champ scalaire direct, profils facettés, traductions, données éditées et exclusions conservées au changement de langue.
- Scénario navigateur opérateur réussi : déplacement souris, orientation, arrêt, créneaux, inversion, portes, acquisition de points, exports, caméra et contrainte de contact sur le cylindre.
- Scénario navigateur limites réussi : extrémités, encombrement du piquage, exclusion étroite, reprise après arrêt partiel, Échap, dépassement manuel avec motif SCAN_LIMIT.
- Scénario navigateur axes/retour réussi : cercle à Z constant, contour autour de l’axe du piquage, orientation locale, remise à zéro de la correction, manipulation des vues, trajet réciproque lié à l’écho courant et suppression en préparation d’examen réel.
- Scénario navigateur EN réussi : boutons, options, champ, labels d’indications et motif d’arrêt.
- Scénario navigateur échos de géométrie réussi : retours heuristiques racine/sommet, absence de retour automatique pour un rebond oblique seul, trajet aller-retour à incidence normale, suppression des signaux synthétiques en préparation d’examen réel.
- Vérification du protocole : géométrie 400/20 mm et piquage 160/12 mm à 63°, plan B −60/+60°, Z −300/+300 mm, recul 35 mm : tour de 144 pas sans arrêt parasite. Plan C, cible MF1 à Az −50°, Z −90 mm, profondeur 10 mm et sonde à Az −50°, Z −100 mm, orientation 0°, angle réfracté 45°, VT 3240 m/s : écho heuristique vers 8,73 µs.

## Corrections de cette livraison

- Dépassement manuel des bornes : arrêt expliqué, au lieu d’une simple limitation silencieuse des coordonnées.
- Réinitialisation : correction d’orientation locale remise à zéro et orientation recalculée en suivi d’axe.
- Listes Usage/Pièce/Souris : recréées au changement FR/EN en conservant leur valeur canonique, pour rafraîchir les libellés dans le navigateur.
- Protocole utilisateur accessible dans Scan manuel, téléchargeable et inclus dans le paquet.
- Brouillons d’évaluation dirigés vers la nouvelle archive ; aucun mail envoyé.

## Fonctions qui restent ouvertes

- Champ acoustique rétrodiffusé par toute la surface du défaut : non implémenté. Le tracé magenta reste une illustration réciproque, pas un champ diffusé calculé.
- Réponse physique complète aux indications, directivité du défaut, diffraction et conversions de modes : non validées.
- Comparaison active Green/Born/Kirchhoff/GTD : non disponible ; sélecteur des modèles futurs désactivé.
- Contact courbe exact, collisions CAO, propagation complète dans la branche et la soudure, couverture acoustique et procédure d’examen : à valider/développer.
- Le champ direct de Green et la réponse A-scan restent des modèles distincts.
- Le protocole utilisateur détaillé est en français, y compris dans son panneau explicitement marqué French en interface EN.

Conclusion d’usage : paquet pour évaluation du geste et de l’explication pédagogique, pas une validation d’examen industriel. Le retour utilisateur sur le réalisme du geste reste nécessaire.
