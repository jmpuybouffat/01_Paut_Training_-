## Retrouver le champ coloré du premier modèle

Onglet **3 · Scan manuel**, panneau **Champ coloré — propagation et réflexions pédagogiques**. Le choix initial **Champ avec réflexions — premier modèle** affiche la carte 0 à −40 dB et les parcours réfléchis, synchronisés au palpeur de surface et à l’A-scan. Le champ est pédagogique : il ne représente pas une mesure ni une simulation élastodynamique validée.

Les choix **Volume 3D calculé** et **Coupe calculée** montrent le champ direct scalaire équivalent, avec phase et fréquence. Le seuil dB règle les points du volume affichés. Dans ces deux modes, le calcul s’arrête à la première interface ; les autres parcours restent géométriques. Le palpeur est commun à toutes les vues. En mode élève, les positions des indications restent cachées.

## Démonstration de formation prête à balayer

Choisir **TRAINING / DEMO_GESTE_PAROI**. Le scénario fournit cinq cibles artificielles de démonstration dans la paroi principale ; ce ne sont pas des positions réelles sur les flancs. Le mode élève masque les indications. Dans l’onglet 3, déplacer la MWB sur la surface 3D ; le faisceau pédagogique transparent et l’A-scan sont côte à côte et synchronisés. Les boutons Créneaux/Pause et Inverser le parcours restent disponibles. Le bouton ±1° et la molette sur le palpeur modifient son orientation. L’éventail coloré reste une représentation géométrique, pas un champ Green/Born/Kirchhoff/GTD.

Choisir **PIECE_PERSONNALISEE** pour saisir les positions de votre propre pièce. Les sections suivantes concernant les positions manquantes s’appliquent à ce mode. **Exporter scène RV** fournit le repère, les poses, les rayons et la scène paramétrique pour l’intégrateur ; voir VR_SCENE_SCHEMA.md.

## Scan de surface 3D — correctif de geste

Dans l’écran manuel, la vue opérateur s’ouvre sur le piquage 3D. Choisir **Déplacer sonde**, saisir le symbole MWB avec le bouton gauche et glisser sur la surface du tube principal. Le point est contraint au cylindre. Les exclusions et l’ouverture arrêtent le déplacement. Pour tourner la pièce, choisir **Tourner pièce** ; la molette dans ce mode zoome. Revenir à **Déplacer sonde** pour scanner ; la molette au voisinage du palpeur règle alors l’orientation. **Déroulé** reste une aide secondaire. Les indications restent cachées sur la vue de surface ; la révélation des vues internes est réservée au mode instructeur.

Les vues géométriques synchronisées ne constituent pas un champ ultrasonore physique. Green, Born, Kirchhoff et GTD restent à implémenter ; voir EXIGENCES_PHYSIQUE_ET_OPERATEUR.md. Les sections suivantes décrivant l’ancien geste sur déroulé restent applicables lorsque cette aide est sélectionnée.

# BYTE NDT — utilisation du twin nozzle REV0.4

Correctif ergonomique : quatre onglets. La vue du piquage est remise en premier ; le planificateur technique ne se confond plus avec le scan manuel.

## 1. Lancer et retrouver le piquage

Extraire le ZIP. Sous Windows, double-cliquer `LANCER_NOZZLE.bat` dans le dossier contenant `app.py`. La première installation nécessite Internet ; garder la console ouverte. Si Streamlit demande une adresse e-mail, laisser vide et appuyer sur Entrée.

L’onglet **1 · Piquage 3D** présente les tubes, parois et intersections issus de REV0.3. Glisser dans la vue fait tourner la pièce ; la molette zoome. Réinitialiser la vue 3D restaure la caméra. Cette action oriente la pièce à l’écran ; elle ne déplace pas la sonde.

## 2. Préparer une pièce test

Choisir FR et TRAINING pour un exercice pédagogique. Dans la barre latérale, régler les deux diamètres extérieurs, les épaisseurs, l’angle entre axes, le décalage et les longueurs ; puis le chanfrein, le jeu, le talon et le renfort. Les unités sont mm et degrés. Le module de matériaux contient des valeurs indicatives à confirmer. Les modèles Kirchhoff/Born/GTD sont dans Modules futurs : ils n’effectuent aucun calcul.

Dans **2 · Réglages de la pièce**, choisir la MWB 45°, 60° ou 70° et la fréquence 2, 4 ou 5 MHz. Cette sélection unique commande le panneau de scan. L’angle MWB est l’angle réfracté nominal dans la pièce ; ce n’est pas l’angle physique du sabot.

## 3. Définir les accès et les limites

Chaque ligne du tableau d’accès décrit une zone de balayage :

- `zone` : nom de la zone ; `reason` : cause d’inaccessibilité, si nécessaire.
- `azimuth_start_deg`, `azimuth_end_deg` : limites autour de l’axe Z du tube principal. Azimut 0° = +X ; 90° = +Y.
- `z_start_mm`, `z_end_mm` : limites le long du tube principal ; origine au milieu de sa longueur.
- `available_length_mm`, `available_width_mm` : place disponible pour le balayage.
- `probe_length_mm`, `probe_width_mm` : dimensions réelles du sabot.
- `travel_mm` : course nécessaire ; `margin_mm` : marge de chaque côté.

Choisir `TO_ASSESS` pour contrôler les encombrements saisis. La longueur nécessaire vaut longueur du sabot + course + deux marges ; la largeur nécessaire vaut largeur du sabot + deux marges.

`FOOTPRINT_FITS_ONLY` signifie que cette comparaison dimensionnelle passe, pas que tout le volume est couvert. `INACCESSIBLE` signifie zone exclue. Une zone inaccessible sans limites bloque tout le plan. `INSUFFICIENT_CLEARANCE` signale un encombrement incompatible. `UNASSESSED` signifie non évalué ; ne pas le présenter comme un accès établi.

Le scan manuel permet de regarder la géométrie du faisceau en zone non évaluée, avec ce statut visible. Les exclusions explicites et l’ouverture du piquage bloquent les rayons. Le planificateur technique peut afficher « sonde non activée » lorsque l’encombrement n’est pas évalué : cela ne signifie pas que l’application est arrêtée.

## 4. Définir le parcours et les cinq indications

Toujours dans l’onglet 2, régler les azimuts de début/fin, Z de début/fin et le pas du plan. Le bouton Créneaux de l’écran opérateur lira ces points. L’orientation du faisceau est mesurée depuis +Z dans le plan tangent local ; elle est distincte de l’angle réfracté MWB.

Nommer la pièce test. Les cinq lignes du registre sont : deux collages/manques de fusion 6 × 3 mm, une inclusion diamètre 2 mm, deux fissures de choc thermique 4 × 2 mm. Dimensions et activation sont modifiables.

Pour chaque indication active, fixer :

- `azimuth_deg` : position autour du tube principal ;
- `z_mm` : position longitudinale ;
- `depth_mm` : profondeur radiale depuis la surface extérieure ;
- `orientation_deg` : orientation locale depuis +Z.

Les cellules doivent être renseignées numériquement ; si les colonnes ne tiennent pas à l’écran, faire défiler le tableau horizontalement. Il n’existe pas encore de placement automatique sur les flancs réels de préparation. Les positions de ces cinq indications n’ont pas été fournies : elles restent vides par défaut, et aucune indication non positionnée ne génère de réponse A-scan. Ne pas confondre le registre projet avec les exemples avancés, indépendants et repliés.

Laisser ces positions vides permet de vérifier le geste et les rayons, mais pas de faire un exercice complet de recherche d’indications. Pour un scénario de formation, définir explicitement des positions virtuelles et les conserver dans l’export de cette pièce ; pour une pièce réelle, utiliser ses données réelles.

## 5. Réaliser le scan manuel

Ouvrir **3 · Scan manuel**. Le tableau de bord comprend le tube principal déroulé, la vue coupe/3D, l’A-scan pédagogique et la projection XY de l’éventail de rayons.

Sur la vue déroulée, saisir le symbole de sonde en maintenant le bouton gauche. Déplacer la sonde sur une première ligne de balayage, décaler légèrement, puis revenir sur une ligne parallèle, et répéter : c’est le mouvement en créneaux. Le tracé bleu montre le chemin du point de sonde. Le bouton Créneaux ▶ lance ou reprend le parcours paramétré ; Pause arrête la lecture et permet de reprendre à la main. Inverser le parcours change le sens de lecture, y compris en cours de lecture, sans tourner la sonde. Tourner sonde 180° change seulement son orientation. À une extrémité, une nouvelle lecture repart du début dans le sens sélectionné. Ce tracé de surface ne constitue pas une démonstration de couverture de tout le volume.

Sur une réponse pédagogique, arrêter le déplacement, puis effectuer une faible rotation avec la molette au voisinage du palpeur, ou les boutons −1° et +1°. Observer la réponse de la porte et le maximum mémorisé. Les réponses actuelles sont heuristiques et ne permettent pas une caractérisation physique validée.

Pour voir la pièce complète, choisir **Nozzle 3D + rayons** dans le sélecteur de la vue coupe. Glisser dans cette vue fait tourner la caméra ; la molette y zoome. Ce geste caméra est distinct du déplacement de la sonde sur la vue déroulée. Vue initiale réinitialise la caméra.

## 6. Enregistrer et exporter

Choisir la porte A, B ou C. Définir début et fin en microsecondes ainsi que le seuil relatif. Un changement de porte ou de bornes remet le maximum affiché à zéro. Enregistrer plusieurs points autour d’une réponse avec le bouton Enregistrer point. L’étendue −6 dB est calculée sur les points enregistrés dans la même porte et pour la même indication synthétique ; ce n’est pas une taille certifiée.

Mode instructeur révèle les indications du registre lorsque leurs positions sont définies. Le mode élève les masque à l’écran.

Exporter depuis le panneau opérateur pour conserver le parcours, les positions, les portes et les mesures pédagogiques. Exporter aussi la fiche de pièce JSON et les CSV souhaités dans l’onglet 2/4. Faire ces exports avant un rechargement ou un changement des paramètres Streamlit : le parcours manuel n’est pas conservé entre deux chargements du panneau.

## 7. État réel de la simulation

La géométrie du piquage et le scan manuel sont raccordés. Les rayons sont tracés dans la paroi cylindrique principale, avec réflexions spéculaires sur les surfaces intérieure/extérieure, arrêt aux extrémités et à l’enveloppe d’ouverture. L’éventail ±5° est illustratif. La propagation complète dans la branche et le volume soudé reste à résoudre ; l’ouverture/préparation n’est pas un solide CAO acoustique validé.

En TRAINING, les réponses d’indications sont pédagogiques et non étalonnées. En REAL_EXAM_PREPARATION, aucune acquisition n’est connectée et aucun signal synthétique n’est affiché comme une mesure réelle. CAD/TCG, cascade, Kirchhoff, Born et GTD restent à raccorder. Le choix d’un nom de modèle ne l’exécute pas.

Le livrable actuel est un démonstrateur de formation en développement, pas un simulateur de qualification ni un système d’examen opérationnel terminé.

L’encart Streamlit « Help agents write better apps » / Install est destiné aux outils de développement. Aucune installation n’est nécessaire pour utiliser le twin. Fermer avec la croix ou « Don’t show again ».

## Échos de base et parcours skip — complément

Le mode élève laisse les sources cachées, mais affiche les signaux pédagogiques de géométrie et d’indications dans l’A-scan. Les profils de racine et de sommet sont déduits des intersections paramétriques du nozzle ; leur rétrodiffusion est représentée par une heuristique non étalonnée, pas par un calcul élastodynamique de ces profils. Une indication peut contribuer sur plusieurs legs si les trajets passent à proximité.

Convention affichée : leg 1 vers la face interne = ½ skip ; leg 2 vers la face externe = 1 skip ; leg 3 vers la face interne = 1½ skip ; leg 4 vers la face externe = 2 skips. Les repères gris du temps de vol correspondent à un aller-retour hypothétique jusqu’à ces positions. Ils ne créent pas automatiquement des échos de fond ou de surface.

Pour les réponses de racine, sommet et indications, le modèle pédagogique suppose une rétrodiffusion sur le chemin réciproque et calcule le temps avec deux fois le parcours jusqu’à la cible. Un retour spéculaire de paroi n’est accepté que lorsque le rayon revient dans la zone de réception du palpeur avec une direction compatible ; son temps utilise le parcours complet déjà tracé, sans le doubler une seconde fois.

La porte initiale s’étend automatiquement pour laisser examiner les doubles skips aux angles élevés. L’opérateur choisit ensuite la porte et ses bornes. Le passage entre vue de coupe et vue 3D utilise les mêmes segments. La géométrie complète de soudure, les coefficients physiques et les conversions de modes restent à développer.

La zone de préparation interdit le placement du palpeur ; elle n’est pas considérée entièrement vide pour la propagation. Le tracé s’arrête dans l’alésage du nozzle, aux limites du tube ou au terme du nombre de legs modélisés. C’est une approximation de domaine, sans solide CAO soudé validé.

## Racine, sommet et description de grains

Dans la barre latérale, le panneau **Racine et sommet — profils facettés de formation** ajuste l’aspect grossier/brisé des bourrelets (amplitude, nombre de facettes et identifiant reproductible). Ce sont des hypothèses de pièce training. Les réponses géométriques tiennent compte des profils et d’une pondération heuristique d’incidence ; ce n’est pas un calcul complet de réflexion sur les faces.

Le panneau **Microstructure — description pour étape suivante** enregistre morphologie, taille et orientation des grains. Ces données sont exportées, mais n’altèrent pas encore les vitesses, le champ ou l’A-scan. Lire RACINE_SOMMET_MICROSTRUCTURE.md pour les limites.
