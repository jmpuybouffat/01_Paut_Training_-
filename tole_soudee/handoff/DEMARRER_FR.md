# BYTE NDT — Tôle soudée P03 🇫🇷

1. Extraire **tout le ZIP** dans un dossier.
2. Double-cliquer sur **OUVRIR_APPLICATION.html**. L’application s’ouvre dans Chrome ou Edge, sans installation et sans connexion Internet.
3. Choisir 🇫🇷 ou 🇬🇧, puis SE, MWB ou PA. « Position témoin » propose une pose d’exercice. Cliquer « Calculer » pour enregistrer la réponse.
4. Pour palper librement, maintenir le bouton gauche de la souris dans le plan et glisser en X et Y. Le sabot et le faisceau suivent le geste ; les réponses calculées sont indexées par leur pose X/Y. Un aperçu du champ est calculé pendant le glissement, puis la grille complète est recalculée au relâchement. Les boutons X−/X+/Y−/Y+, le pas réglable et les flèches du clavier (plan sélectionné) permettent les petits mouvements. « Zoom soudure » facilite le réglage transversal ; « Tôle entière » restitue la vue globale. Le trait bleu représente l’encombrement provisoire du sabot, marge comprise. Une collision suspend le calcul et l’enregistrement.
5. Les créneaux progressent selon X par pas de 2 mm, puis s’indexent en Y. Arrêt et effacement sont disponibles. Inverser l’orientation et placer le sabot de l’autre côté pour examiner depuis les deux rives.
6. « Préparation examen » masque les indications et la position témoin. Renseigner opérateur, référentiel et rapport. Exporter la session et le rapport. Il s’agit d’un exercice local, pas d’un examen sécurisé ou d’une qualification officielle.

Le calcul initial n’est pas enregistré. Chaque calcul de palpage terminé ou pose de créneau ajoute une acquisition. Pendant un glissement, les positions intermédiaires sont regroupées si le calcul est occupé ; ce prototype ne garantit pas une cadence vidéo ni un pas de 2 mm en mode libre. Le pas de 2 mm concerne les créneaux. Changer de langue conserve les acquisitions. Changer de mode formation/examen efface les acquisitions pour éviter de mélanger les exercices.

## Ce qui est livré

CAO 245 × 250 × 10 mm, préparation en X à 45°, bourrelets et ZAT ; cinq indications de scénario ; modes SE à deux cristaux, MWB 45/60/70° et PA 32 éléments 5 MHz ; secteur 35–70° ; A-scan enveloppe, axe en coupe Y–Z, champ scalaire incident/diffusé, S-scan rétroprojeté, B-scan par numéro de pose et cumul 3D. Le B-scan emploie le premier rayon du secteur PA ; les autres rayons restent dans la session exportée.

Matériau nominal type A42 : VL 5 920 m/s, VT 3 240 m/s, masse volumique 7 850 kg/m³. Mêmes propriétés de départ dans la soudure et les ZAT : pas d’échos artificiels aux frontières des ZAT. E7018 est une famille de métal d’apport illustrative, pas un mode opératoire qualifié.

PA retenu : Imasonic, 32 éléments, 5 MHz, pitch 0,5 mm, élévation 12 mm. Largeur d’élément provisoire 0,45 mm ; focalisation dans l’acier provisoire à 30 mm de trajet acoustique. Sabot nominal 55° T dans l’acier. La référence et la géométrie réelles du sabot ne sont pas encore fournies : le calcul part de l’interface acier. Les encombrements mécaniques et les sondes SE/MWB restent des valeurs de démonstration.

## Lecture des vues

L’A-scan est une enveloppe synthétique d’amplitude relative, avec une échelle verticale fixe 0–1 après gain. Réduire le gain si un pic dépasse l’échelle ; augmenter le gain pour rechercher de faibles réponses. La couleur du S-scan et du cumul est en dB de cette référence relative, pas en dB d’une référence d’étalonnage réglementaire.

Deux cartes séparées montrent le champ incident avec réflexion sur le fond, puis le champ diffusé calculé (retour vers la sonde inclus). Le champ diffusé somme les contributions complexes des indications actives. Les deux utilisent une référence scalaire fixe commune (0,05 dans les unités du propagateur) et une palette pédagogique proche de CIVA, de −60 à 0 dB ; ce n’est ni une LUT constructeur vérifiée ni une pression calibrée. Les rayons centraux sont superposés. La profondeur vaut 0 sur la face de palpage ; le Z global reste utilisé dans la CAO, les poses et les sections géométriques. Les positions de défauts affichées sont la vérité du scénario, pas une reconstruction. Le S-scan et le cumul 3D sont des rétroprojections temps-angle, avec ambiguïtés de trajet.

## Limites à conserver pendant la revue

Le modèle scalaire à fréquence centrale emploie une ouverture finie, une approximation de surface pour les plans et une approximation de Born faible pour les inclusions. Une image sur la face opposée est autorisée par trajet émission/réception. Les impulsions sont synthétiques ; la réponse large bande complète n’est pas calculée. Il n’y a pas encore de propagation dans le sabot, de conversion de mode, de diffraction GTD, de diffusion des bourrelets ou de calcul élastique complet. Les échos de fond reçus sont calculés pour SE/MWB ; leur calcul PA n’est pas inclus dans cette version.

Avant un usage de préparation de certification, faire valider le scénario, la couverture, les réglages de sensibilité et le référentiel par le formateur. Cette première livraison permet la revue du geste et des vues ; elle ne valide pas la détection ni l’acceptabilité de toutes les indications.

## Pour Fabien

Le dossier **FABIEN_CAMERA** contient le contrat de données, sans casque. La détection par caméra et la calibration image/tôle sont à raccorder à son système ; elles ne sont pas implémentées par ce fichier. Le panneau de liaison permet de tester une pose JSON déjà calibrée. Aucune compétence de programmation n’est demandée au stagiaire.

## Corrections de palpage P03

Le contour du sabot est rectangulaire (ordre des sommets corrigé). La coupe dédiée montre la préparation **en X** et les deux bourrelets ; la coupe du faisceau superpose le même profil au trajet réfléchi. Le V éventuel de la ligne bleue est le trajet de propagation, pas un chanfrein en V. La géométrie STEP en X reste la référence.

## Vues et déplacements P03

Le cadrage et la caméra sont conservés entre les pas X/Y, y compris après un zoom manuel. « Réinitialiser les vues » restitue les cadrages initiaux ; « Zoom soudure » et « Tôle entière » changent volontairement le plan de palpage. Les boutons du haut X−1 et X+1 déplacent maintenant de 1 mm ; les créneaux conservent le pas X de 2 mm. Les cartes de champ ont une fenêtre Y fixe 70–180 mm. Le calcul harmonique et l’aperçu en déplacement puis le recalcul complet au relâchement restent ceux du prototype scalaire.
