# Bilan de vérification — RÉTRO SCALAIRE

Livraison technique pour revue par l’utilisateur. Pas de diffusion aux évaluateurs ni de mail envoyé. Les vérifications portent sur la cohérence et le fonctionnement du modèle réduit, pas sur un instrument UT ou un examen industriel.

## Nouveau modèle

Surface plane finie pour MF/fissures, sphère réfléchissante pour INC1. Excitation cohérente par ouverture MWB, intégration complexe de Kirchhoff scalaire, puis réception moyennée sur la même ouverture. Pas de normalisation à chaque pose. Enveloppe A-scan issue de cette réception ; temps de centre géométrique. Travail asynchrone : les résultats d’une pose ancienne sont retirés, et l’enregistrement attend le résultat courant.

## Vérifications scientifiques et numériques

Tests du noyau JavaScript, identique à celui embarqué dans le navigateur :
- conservation de la surface quadraturée ;
- convergence en raffinant les quadratures émission et surface ;
- superposition complexe et annulation par opposition de phase ;
- réciprocité émission/réception sur deux ouvertures finies ;
- modification de la réception monostatique par inclinaison de la face ;
- échelle dB fixe : doubler l’amplitude ajoute 6,02 dB ;
- zéro de diffraction rectangulaire conforme à l’approximation analytique de Fraunhofer ;
- éclairage d’un hémisphère avec normales propres pour une sphère ;
- surface vide et entrées invalides.

## Vérifications de l’application

- 22 tests Python/Streamlit : géométrie, plans, champ direct, profils, données/traductions et chargement du témoin avec normale de face.
- Nouveau scénario Chromium : champ de coupe/volume non uniforme, données de facettes finies, couplage exact entre amplitude intégrée et événement A-scan, modifications d’orientation et de fréquence, référence fixe, gestion des portes, désactivation du défaut, préparation d’examen réel, absence de résultats périmés, calcul dans iframe sandbox et zoom sur la cible.
- Scénarios existants : gestes/souris/roulettes, créneaux, arrêt, inversion, limites, zones exclues étroites, reprise après arrêt partiel, deux axes, correction angulaire, caméras, exports, FR/EN et anciens échos racine/sommet.

Témoin : tube 400/20 mm, MWB 45°/4 MHz, VT 3240 m/s, MF1 6 × 3 mm à Az −50°, Z −90 mm, profondeur 10 mm, normale inclinée 45° ; sonde à Az −50°, Z −100 mm, orientation 0°. Résultat : temps de centre 8,73 µs, amplitude relative environ 0,0619 (−24,2 dB pour référence 0,05). Surface : 276 facettes à λ/3 ; coupe : 2584 cellules ; volume : 1547 points sur la grille retenue. Le champ n’est pas une image gaussienne reconstruite depuis l’amplitude de l’écho.

## Limites ouvertes

Incidence directe et diffusion unique seulement. Pas de rebonds du champ diffusé sur ID/OD, pas de diffraction élastique, conversions L/T, sabot/contact complet, contrastes d’inclusion, interaction entre défauts ou propagation complète soudure/branche. L’enveloppe graphique n’est pas une simulation large bande de la chaîne d’acquisition. Les échos heuristiques de racine/sommet ne sont pas mélangés à la nouvelle enveloppe scalaire.

Le test utilisateur sur le réalisme et la pertinence pédagogique reste requis. La présence d’un champ calculé ne constitue pas une qualification industrielle ni une validation équivalente CIVA.

Le protocole utilisateur est désormais intégralement disponible en français et en anglais ; le panneau et son téléchargement suivent la langue sélectionnée.
