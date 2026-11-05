# CAO de référence — tôle soudée à préparation en X

## Ouvrir les fichiers

- **CAD_TOLE_X_FR_EN.html** : visionneuse autonome, à ouvrir dans le navigateur après extraction du ZIP. Aucun serveur ou logiciel Python requis. Drapeaux 🇫🇷/🇬🇧, vue 3D, coupe nominale Y–Z, zoom soudure et visibilité des régions/indications.
- **TOLE_X_245_250_10_ASSEMBLAGE.step** : assemblage détaillé à ouvrir dans Fusion, avec bourrelets striés et pièces nommées.
- **WELDED_PLATE_X_245_250_10_ASSEMBLY_EN.step** : même assemblage avec noms des composants en anglais.
- **TOLE_X_ENVELOPPE_LISSE.step** : enveloppe sans stries pour les contrôles simples ou un import plus léger.
- **INDICATIONS_REFERENCES_NON_COUPANTES.step** : géométrie enseignante séparée. Deux faces de collage, deux sphères et une face de fissure dentelée. Aucun vide d’ouverture arbitraire n’est créé dans le métal.
- **PIECES/** : fichiers STEP séparés pour les neuf régions solides.
- **variations_indications.csv** : table numérique canonique des paramètres initiaux.
- **variations_domaines.csv** : paramètres et colonnes de bornes à compléter avant génération des variantes.
- **table_indications_FR.csv / table_indications_EN.csv** : tableaux lisibles dans chaque langue.
- **geometrie_pour_rv.json** : triangles, noms, couleurs et coordonnées en mm pour la reprise graphique/RV ; ce fichier ne contient pas de simulation acoustique.
- **SOURCE/** : code de génération, paramètres et vérifications.

## Valeurs géométriques retenues

Tôle 245 × 250 × 10 mm. X longitudinal, Y transversal, Z dirigé de la face inférieure à la face supérieure ; origine dans un coin de la face inférieure. Axe soudure Y = 125 mm. Quatre faces à 45°, talon central 1,25 mm, jeu de préparation 1 mm. Talon variable entre 1 et 1,5 mm.

La préparation symétrique a une profondeur de 4,375 mm par face, une largeur de 9,75 mm aux faces extérieures et un talon entre Z = 4,375 et 5,625 mm. Le jeu entre les tôles est rempli par le métal fondu dans le modèle soudé.

Bourrelets supérieur et inférieur : largeur 18 mm, surépaisseur maximale 2,5 mm, rayon circulaire nominal 17,45 mm. Pieds à Y = 116 et 134 mm ; sommet supérieur Z = 12,5 mm, inférieur Z = −2,5 mm.

ZAT représentées par deux bandes de 10 mm au-delà des pieds : Y = 106–116 et 134–144 mm. Ce sont des régions géométriques ; aucune différence de vitesse acoustique n’est encore attribuée.

Les neuf solides partitionnent le volume sans superposition : base extérieure, ZAT et rive de chaque côté, métal fondu et deux bourrelets. Les interfaces entre régions sont partagées ; elles ne représentent pas des lames d’air.

## Détails proposés, à examiner

Les stries ont un pas de 3 mm, une largeur de 0,12 mm, une profondeur maximale de 0,08 mm et une flèche d’arc de 1 mm. Ces valeurs illustratives ne proviennent pas d’un relevé réel. Les deux bourrelets comportent chacun 81 stries courbes peu profondes, construites dans la CAO, sous l’enveloppe circulaire nominale.

MF1 et MF2 : longueurs 2 et 4 mm, largeur de face prise provisoirement à 0,5 mm ; faces effectivement placées sur les chanfreins. L’ouverture normale de la lame d’air reste non définie. INC1/INC2 : diamètre 0,5 mm, positions proposées dans les bandes ZAT. FIS1 : référence dentelée de longueur 2 mm et encombrement transversal 0,5 mm, détails et position proposés.

Les coordonnées et orientations de ces cinq références sont un scénario de départ, pas des défauts mesurés ni des positions déjà validées. Les faces de référence restent séparées de l’assemblage physique. Le sens de « largeur 0,5 mm » et l’ouverture des collages/fissure doivent être confirmés avant la représentation acoustique finale.

## Orientation et suite logicielle

Angles en degrés, convention R = Rz × Ry × Rx ; la face locale de référence est dans XY avec normale +Z. La matrice équivalente et les coordonnées partagent le repère de la pièce.

Le programme prévu conserve SE 0° à deux cristaux, MWB 45/60/70°, puis PA 1D 32 éléments à 5 MHz, sectoriel 35–70°. Le S-scan est dans Y–Z ; le déplacement et le cumul des coupes se font selon X, avec pas spatial initial 2 mm. Le pas angulaire est distinct et reste à définir.

**Cette livraison est la CAO et sa visionneuse. Elle ne contient pas encore l’application de palpage, les lois PA ou les champs ultrasonores.** Le matériau, les propriétés acoustiques, les références/dimensions des sondes et sabots restent à préciser. L’application Nozzle existante est un projet distinct.

## Régénérer la CAO

Pour l’équipe de développement uniquement : installer les dépendances de requirements-cad.txt, modifier parameters.json puis lancer `python cad_model.py` et `python make_viewer.py`. La source est paramétrique ; le STEP échange des géométries, il ne reconstruit pas un historique paramétrique natif Fusion.

Les exports sont vérifiés par validité des solides, volumes sans chevauchement, profil analytique et réimport du STEP. Voir BILAN_CONTROLES_FR_EN.md.
