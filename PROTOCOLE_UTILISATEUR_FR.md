# Protocole utilisateur — scan manuel monoélément

Version RÉTRO SCALAIRE. Objectif : vérifier le geste, les limites, la synchronisation et le modèle réduit de diffusion. Ce protocole ne valide pas un examen UT industriel. Pour commencer le nouveau champ : voir RETRODIFFUSION_SCALAIRE_FR_EN.md et le bouton Charger le test témoin dans Scan manuel.

## 1. Préparation commune

Avant de changer les réglages de la pièce, exporter les points déjà acquis avec Exporter JSON. Un changement Streamlit peut reconstruire le panneau et effacer la session de scan. Ne pas modifier les réglages pendant un scan.

Dans la barre latérale :

| Réglage | Valeur |
|---|---|
| Langue | FR |
| Usage | Formation |
| Pièce de formation | Démo de balayage en paroi pour les tests de geste |
| Diamètre extérieur tube principal | 400 mm |
| Épaisseur principale | 20 mm |
| Diamètre extérieur nozzle | 160 mm |
| Épaisseur nozzle | 12 mm |
| Angle entre axes | 63° |
| Décalage transversal | 0 mm |
| Longueur tube principal | 800 mm |
| Longueur nozzle extérieure | 320 mm |
| Angle de chanfrein / jeu / talon | 35° / 2 mm / 2 mm |
| Largeur nominale du cordon / surépaisseur | 14 mm / 3 mm |
| Matériau | Acier carbone |
| VL / VT / masse volumique | 5920 m/s / 3240 m/s / 7850 kg/m³ |

Dans 2 · Réglages de la pièce : choisir la configuration MWB nominale 45° / 4 MHz. Dans le tableau des zones, garder Zone 1 avec Accès = Non évalué et aucune exclusion pour commencer. « Non évalué » autorise ici l’exploration géométrique mais ne prouve pas l’accessibilité réelle.

Ne pas modifier Green/Kirchhoff/GTD : ce sélecteur de modules futurs n’est pas un comparateur de calculs actifs.

Dans 3 · Scan manuel :
- Cliquer STOP / Pause puis Réinitialiser.
- Champ et rayons : coché. Instructeur : décoché. Retour indication pédagogique : décoché.
- Trajectoire : Libre ; Orientation locale : 0°.
- Surface : Piquage 3D — déplacer la sonde ; Geste : Déplacer sonde.
- Porte : A ; Début : 0 µs ; Fin : 80 µs ; Seuil relatif : 0,01 ; Gain : 3.
- Dans le panneau Champ, choisir Champ avec réflexions — premier modèle ; seuil −30 dB.

Attention : « Souris 3D / Rotation libre » dans la barre latérale commande la caméra de la pièce. « Trajectoire / Libre » dans le scan commande le geste de la sonde. « Pièce personnalisée » commande le contenu du spécimen, pas la liberté du geste.

## 2. Trois plans de scan à utiliser

Saisir les valeurs dans 2 · Réglages de la pièce → Scan géométrique — tube principal. Conserver Pas de scan = 10 mm, Marge géométrique = 2 mm et Orientation du faisceau depuis +Z = 0° dans tous les cas.

| Plan | Azimut début | Azimut fin | Z début | Z fin | Usage |
|---|---:|---:|---:|---:|---|
| A | −60° | −40° | −180 mm | −120 mm | Geste libre, créneaux et bornes, loin du piquage |
| B | −60° | +60° | −300 mm | +300 mm | Suivi autour du piquage et approche de son encombrement |
| C | −50° | −30° | −100 mm | −60 mm | Réponse d’une cible témoin personnalisée |

Retourner dans Scan manuel après chaque changement et cliquer Réinitialiser. Le point initial reprend Azimut début et Z début. Az, Z et θ dans la ligne d’état sont des mesures de la pose courante, pas des champs à saisir.

## 3. Test 1 — geste libre et orientation

Réglages : plan A ; Trajectoire Libre ; Orientation locale 0° ; Geste Déplacer sonde.

Saisir le symbole MWB et le déplacer au milieu de la zone. Cliquer +1° cinq fois, puis −1° cinq fois. Essayer la molette au-dessus du symbole. Essayer Tourner sonde 180°.

Attendu : Az/Z changent pendant le déplacement ; θ change pendant la rotation ; faisceau, coupe, champ et A-scan se mettent à jour. L’angle MWB nominal reste 45° : θ est l’orientation de la sonde dans le plan tangent, pas l’angle réfracté.

Si la sonde est sur la face cachée, choisir Geste → Tourner pièce, tourner la caméra, puis revenir à Déplacer sonde. La caméra seule ne doit pas changer Az/Z/θ.

## 4. Test 2 — fin de créneaux, inversion et reset

Réglages : plan A ; Libre ; Réinitialiser.

Cliquer Créneaux, laisser atteindre la fin du parcours, puis cliquer Inverser le parcours et Créneaux. Tester STOP / Pause pendant le mouvement. Relancer puis tester Échap, avec le focus dans le panneau de scan. Enfin cliquer Réinitialiser.

Attendu : pas de boucle infinie ; arrêt à la fin ; retour en sens inverse ; pause immédiate ; reset à Az −60°, Z −180 mm, θ 0°, avec effacement des points et du maximum mémorisé. Exporter avant reset si nécessaire.

## 5. Test 3 — limites du plan

Réglages : plan A ; Libre. Surface → Déroulé — aide secondaire pour lire les bornes plus facilement.

Glisser vers chacun des quatre bords puis essayer de dépasser. Revenir vers l’intérieur.

Attendu : point d’entrée maintenu entre −60° et −40°, Z entre −180 et −120 mm ; retour vers l’intérieur possible. Une tentative de dépassement arrête le geste avec le motif « limite du plan » ; saisir à nouveau la sonde pour repartir vers l’intérieur. Les limites du plan concernent le point d’entrée ; elles ne garantissent pas que tout le sabot reste à l’intérieur du rectangle du plan.

## 6. Test 4 — axe du tube principal

Réglages : plan B ; Réinitialiser ; Trajectoire → Axe tube principal ; Orientation locale 0°.

Noter Z. Cliquer Parcours + dix fois, puis Parcours − dix fois. Essayer de glisser la sonde verticalement dans la vue de surface.

Attendu : déplacement circonférentiel avec Z constant. Az varie. Orientation locale reste réglable. Le Z ne suit pas le glissement vertical dans ce mode.

## 7. Test 5 — axe du piquage et orientation locale

Réglages : plan B ; Réinitialiser ; Trajectoire → Axe piquage ; Recul soudure 35 mm ; Orientation locale 0°.

Cliquer Parcours + pour rejoindre le contour. Continuer par clics successifs pour parcourir le contour complet. Vérifier simultanément Az, Z et θ. Essayer Parcours −. Puis changer Orientation locale à +10°, revenir à 0°, puis −10°.

Attendu : Az ET Z varient autour du piquage ; θ suit la direction vers la soudure. L’écart manuel s’ajoute à cette direction. La sonde reste sur le tube principal. Le tour n’est possible que si le plan et l’encombrement le permettent.

Essayer ensuite Recul soudure 50 mm. Cliquer Parcours + pour rejoindre le nouveau contour. Le rayon de l’enveloppe coaxiale change ; ce réglage n’est pas une distance de surface constante à la soudure. Un raccord arrêté avant le contour doit être signalé, sans traverser une zone interdite.

Créneaux est réservé au mode Libre. En mode d’axe, utiliser le glissement et Parcours ±.

## 8. Test 6 — arrêt contre le piquage

Réglages : plan B ; Réinitialiser ; Libre ; Orientation locale 0° ; Surface → Déroulé.

Depuis la position initiale, avancer à Z voisin de −300 mm vers Az voisin de 0°, puis remonter progressivement Z vers le piquage.

Attendu : arrêt avant que l’enveloppe approximative du sabot ne traverse la zone piquage/soudure, avec motif d’arrêt. Repartir dans la direction opposée doit être possible. Le contrôle reste une approximation de rectangle centré 24 × 14 mm, marge 2 mm ; ce n’est pas une collision CAO ni une validation du contact courbe.

## 9. Test 7 — zone volontairement inaccessible

Réglages : plan A. Dans le tableau des zones de l’onglet 2, ajouter une ligne :

| Colonne | Valeur |
|---|---|
| Zone | Test exclusion |
| Accès | Inaccessible |
| Motif | Obstacle témoin |
| Azimut début / fin | −52° / −48° |
| Z début / fin | −160 / −140 mm |

Valider la dernière cellule, puis retourner au scan, Libre, Réinitialiser. Avancer vers cette zone, manuellement ou avec Créneaux.

Attendu : arrêt pour zone exclue avant que l’enveloppe du sabot ne la traverse. Le symbole peut s’arrêter avant la bordure rouge à cause de sa marge. Ne pas laisser les bornes vides : une exclusion sans bornes bloque tout le plan.

Après l’essai, supprimer la ligne Test exclusion, ou remettre Accès → Non évalué. Vérifier qu’aucune exclusion ne subsiste avant les tests suivants.

## 10. Test 8 — cible témoin et A-scan

Ce test utilise une cible artificielle éloignée du piquage pour éviter de confondre réponse d’indication et retour de racine/sommet.

Dans la barre latérale : choisir Pièce personnalisée. Garder la géométrie commune. Dans l’onglet 2, régler le plan C. Dans Bibliothèque d’indications et placement :

| Réglage | Valeur |
|---|---|
| MF1 activée | Oui |
| MF1 longueur / largeur | 6 / 3 mm |
| MF1 azimut | −50° |
| MF1 position Z | −90 mm |
| MF1 profondeur | 10 mm |
| MF1 orientation | 0° |
| MF1 inclinaison normale | 45° |
| MF2, INC1, FCT1, FCT2 activées | Non |

Les cellules de position sont initialement vides en personnalisé : les renseigner toutes pour MF1. Le champ Emplacement est descriptif ; les coordonnées numériques déterminent la cible. Cette position n’est pas un flanc de soudure réel.

Dans Scan manuel : Libre, Réinitialiser, Orientation locale 0°. Vérifier Az −50°, Z −100 mm, MWB 45° / 4 MHz. Choisir l’ancien Champ avec réflexions — premier modèle pour ce test heuristique, puis cocher Instructeur. Porte A, Début 0, Fin 20 µs, seuil 0,01, gain 3.

Attendu : écho MF1 voisin de 8,7 µs avec VT = 3240 m/s, selon le modèle heuristique actuel. Ne pas comparer à une mesure étalonnée. Tourner de quelques degrés et déplacer légèrement la sonde : la réponse doit varier. Pour comparer les positions, observer le signal courant ; le Maximum mémorisé conserve volontairement une valeur passée.

## 11. Test 9 — champ rétrodiffusé calculé

Exporter d’abord les données à conserver. Dans Scan manuel, cliquer **Charger le test témoin rétrodiffusion — MWB 45° / 4 MHz**. Il remplace géométrie, plan, zones et indications. Le mode Champ rétrodiffusé calculé — scalaire est sélectionné.

Attendre la fin du calcul, puis cliquer Zoom indication calculée. Porte A 0–20 µs, seuil 0,01, gain 3 ; seuil du champ −40 dB. Attendu : surface finie rose, lobes colorés, réception scalaire sur l’ouverture ; écho MF1 vers 8,73 µs, amplitude relative voisine de 0,062 dans ce modèle. La référence dB reste fixe, même si la pose change.

Tester l’orientation de sonde, puis l’inclinaison de la normale de MF1 (45° puis 80° dans l’onglet 2), et la fréquence (4 puis 5 MHz). Le champ et la réception doivent changer. Pendant un calcul, aucun champ de l’ancienne pose n’est conservé et Enregistrer point est désactivé.

Une porte à 30–40 µs écarte l’écho direct de MF1, mais ne modifie pas le champ monochromatique. MF1 désactivée : pas de réponse d’indication. Les données de géométrie racine/sommet ne sont pas mélangées à cet A-scan scalaire.

Le calcul inclut une diffusion scalaire sur surface finie, avec phase et ouverture émission/réception. **La diffusion élastique complète et ses rebonds sur les parois ne sont pas implémentés.** Voir RETRODIFFUSION_SCALAIRE_FR_EN.md pour les formules, réglages et limites. L’ancien retour magenta reste uniquement un trajet illustratif dans l’ancien mode pédagogique.

## 12. Test 10 — coupe, champ et caméra

Réglages : cible témoin, plan C, Libre ; Réinitialiser.

Dans la coupe projetée, glisser horizontalement sur quelques pixels puis utiliser la molette. Refaire dans la carte de champ. Observer la pose, le faisceau et l’A-scan. Dans Vue → Nozzle 3D + rayons, glisser puis zoomer.

Attendu : coupe et champ déplacent/orientent la même sonde ; la vue filaire 3D fait tourner/zoomer la caméra sans déplacer la sonde. La coupe Z/profondeur peut comprimer un trajet circonférentiel : utiliser le 3D pour l’interpréter.

Changer le choix Champ de la carte vers Coupe calculée ou Volume 3D calculé, si disponibles : il s’agit du champ direct scalaire de Green, pas du champ rétrodiffusé. Les comparer à la carte pédagogique en tenant compte de cette différence de modèle. Restaurer le champ pédagogique pour les autres essais.

## 13. Test 11 — enregistrement et langues

Sur une réponse, Enregistrer point ; tourner de +1°, enregistrer à nouveau. Vérifier le compteur puis Exporter JSON. Exporter scène RV pour l’évaluation des poses et des arrêts par Fabien.

Exporter AVANT de changer de langue. Passer en EN : vérifier les titres, boutons, types, colonnes et coordonnées du tableau. Les dimensions et indications doivent être conservées. Le scan peut être reconstruit : la conservation de sa trace n’est pas garantie. Revenir en FR.

Noter séparément tout libellé resté français en EN. Une traduction manquante ne doit pas être confondue avec une modification des données.

## 14. Test 12 — séparation avec l’examen réel

Exporter d’abord le scan, puis choisir le mode de préparation d’examen réel dans Usage. Il n’y a aucune acquisition instrument connectée.

Attendu : aucun signal synthétique présenté comme signal réel, aucun retour pédagogique d’indication. Revenir en Formation pour les essais pédagogiques.

## Fiche de retour utilisateur

Pour chaque essai : numéro du test, réussi / anomalie / non essayé, plan A/B/C, sonde, trajectoire, Az/Z/θ, résultat observé, motif d’arrêt, capture si utile. Indiquer la version AXES ET RETOUR.

Évaluer séparément le champ scalaire calculé et le besoin restant de diffusion élastique avec rebonds sur les parois. Le seul retour magenta ne valide aucun de ces calculs.
