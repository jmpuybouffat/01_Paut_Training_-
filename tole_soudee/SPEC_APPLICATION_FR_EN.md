# Tôle soudée — contrat de reprise de l’application / Training app specification

## Géométrie et repères / Geometry and frames

Référence : parameters.json, assemblage STEP et matrice d’indications. X longitudinal à la soudure, Y transversal, Z épaisseur vers le haut. Toutes les longueurs sont en mm. Origine au coin inférieur ; axe de soudure Y = 125 mm. La scène graphique, la simulation et l’export RV doivent employer le même repère. Le facteur mm → m pour un client RV est 0,001 ; aucune autre transformation ne doit être implicite.

Reference geometry is shared by CAD, simulation and VR export. Longitudinal X, transverse Y, upward Z; all lengths in mm. Weld axis Y = 125 mm. Explicit 0.001 mm-to-m conversion for VR, with no hidden recentering or scale change.

## Acquisition prévue / Planned acquisition

- SE 0° : deux cristaux distincts émission/réception, ouverture, écartement et angles de toit à documenter ; représenter leur zone de recouvrement.
- MWB 45°, 60°, 70° : référence, fréquence, pastille, sabot, point d’émergence et encombrement réel à documenter.
- PA linéaire 32 éléments, 5 MHz : catalogue constructeur vérifiable, pitch, dimensions des éléments, sabot, ouverture active et lois focales à renseigner ; sectoriel 35–70°. Pas angulaire en degrés, distinct du pas spatial de déplacement.
- Pas spatial initial 2 mm selon X ; acquisition en Y et positionnement de chaque rayon conservés pour la cartographie.

Dual-crystal SE, MWB and 32-element PA are different source/receiver models. Probe and wedge references must be verified rather than inferred from a generic visual symbol. Spatial step and angular increment are separate parameters.

## Gestes / Operator motion

Déplacement libre et créneaux sur les deux côtés de la soudure, orientation manuelle, arrêt/reprise/inversion/reset. Limites basées sur l’empreinte orientée du sabot et le point d’émergence, bords de tôle et bourrelets ; gestion du contact et de la levée. L’orientation vise la soudure depuis chaque côté. Prévoir le choix de face supérieure/inférieure avec des normales cohérentes.

Free/raster motion, manual skew and geometric stops use actual wedge footprint and exit-point offset. Contact, lifting and face selection must be explicit.

## Vues / Views

A-scan mono ; coupe Y–Z et accumulation mécanique. En PA : S-scan Y–Z du sectoriel, B-scan du déplacement et A-scan du rayon choisi. Le déplacement longitudinal X accumule les coupes en une cartographie 3D des réponses. Distinguer positions connues du simulateur, réponses acquises et reconstruction : une vue cumulée ne doit pas révéler automatiquement la vérité des défauts au stagiaire.

PA Y–Z S-scan, motion B-scan and selected-ray A-scan. X-indexed sections produce an accumulated 3D response map; preserve the difference between simulator ground truth and reconstructed observations.

## Acoustique / Acoustics

Champ incident, réponses de géométrie et champ diffusé/reçu doivent être identifiables et cohérents avec les signaux. Prévoir les trajets directs et les réflexions sur les deux faces. Une convention commune de temps, modes, phase et référence d’amplitude est nécessaire. Ne pas renormaliser l’échelle à chaque pose.

Green est un propagateur ; les réponses de surface, de faible contraste et de diffraction nécessitent des modèles et domaines de validité appropriés. Une lame d’air n’est pas une inclusion de faible contraste. Les moteurs internes C1/C2 ne sont pas présents dans les dépôts publics examinés ; leur raccordement nécessite leurs sources ou des références de calcul adaptées. Aucun moteur complet Born/GTD/élastique n’est déclaré implémenté dans cette livraison.

Incident/scattered fields and the received signal require a coherent model including relevant wall paths. Green propagation and scattering/diffraction operators are distinct. Model validity, phase/time conventions and a fixed amplitude reference must be documented. Full internal C1/C2 engines have not been supplied or connected here.

## Indications, variantes et ML / Flaws, variants and ML

Cinq références initiales, avec X/Y/Z, longueur/largeur/diamètre/ouverture et Rx/Ry/Rz (Rz Ry Rx). Conserver vérité géométrique, paramètres d’acquisition et réponses séparés. Domaines de variation à valider ; garder les identifiants de scénarios et les graines si des variantes sont générées. Séparer entraînement et évaluation par pièce/scénario.

Keep flaw ground truth, acquisition settings and response data separate. Validate variation domains and keep scenario lineage; split ML training/evaluation by specimen/scenario.

## Langues et RV / Languages and VR

🇫🇷 FR et 🇬🇧 EN pour les commandes, tableaux, annotations, unités, protocoles et exports lisibles. Les clés numériques/canoniques restent stables. Préparer les poses 6D, états de contact, arrêts, empreintes, données de champ et traces pour Fabien ; l’export est une interface de données, pas une application immersive terminée.

Both languages cover the whole user flow. Stable canonical keys and shared coordinates support VR integration without claiming that a complete immersive client is already delivered.

## En attente / Pending

P01 fournit maintenant une première application opérateur scalaire, une trame de procédure, le mode préparation examen et une interface de poses caméra pour Fabien, sans casque. Voir handoff/DEMARRER_FR.md et handoff/FABIEN_CAMERA_FR_EN.md pour les fonctions et limites vérifiées. Acier type A42 nominal : VL5920, VT3240 m/s, densité7850 ; mêmes valeurs tôle/soudure/ZAT. PA Imasonic 32 éléments 5 MHz, pitch0,5 mm, élévation12 mm, sabot nominal55° T ; propagation dans le sabot non calculée. Restent à préciser : références exactes des sondes/sabot, géométrie et vitesse du sabot, ouverture des défauts et détails des scénarios. Le raccordement de la détection caméra et sa calibration restent à réaliser avec Fabien.

P01 now supplies a reduced scalar operator prototype, an exercise procedure/report, exam-preparation mode and a camera-pose interface without a headset. Nominal A42 properties and selected PA concept are configured. Exact hardware references, wedge propagation and camera detection/calibration remain pending. See the bilingual handoff documents for verified scope and limitations.
