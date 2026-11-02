# Champ rétrodiffusé calculé — modèle scalaire réduit

## Ce qui change

Le mode **Champ rétrodiffusé calculé — scalaire** calcule un champ complexe émis par une surface d’indication de dimensions finies. Ce n’est pas le tracé magenta épaissi : les contributions des facettes ont une amplitude et une phase, interfèrent dans l’espace et sont intégrées sur l’ouverture de réception MWB.

Le champ direct de Green, l’ancienne carte de réflexions et le retour magenta restent des modes distincts. En mode rétrodiffusé, l’A-scan montre une enveloppe relative provenant de la réception calculée. Les échos heuristiques de racine/sommet ne sont pas ajoutés à ce signal scalaire.

## Essai reproductible en un clic

1. Exporter les données personnelles à conserver. Dans **3 · Scan manuel**, cliquer **Charger le test témoin rétrodiffusion — MWB 45° / 4 MHz**. Ce bouton remplace géométrie, plan, zones et indications par le cas témoin.
2. Le cas utilise le tube 400 × 20 mm, le piquage 160 × 12 mm à 63°, VT 3240 m/s ; MWB 45° / 4 MHz, ouverture nominale 8 × 9 mm. Une seule face MF1 de 6 × 3 mm est activée : Az −50°, Z −90 mm, profondeur 10 mm, orientation 0°, inclinaison de normale 45°.
3. La sonde démarre à Az −50°, Z −100 mm, orientation 0°. Choisir **Champ rétrodiffusé calculé — scalaire** si nécessaire, cible MF1 ou Réception maximale, seuil de champ −40 dB.
4. Attendre la fin du calcul. Pendant le calcul, les anciens résultats sont retirés et Enregistrer point est désactivé. Le déplacement reste possible.
5. Cliquer **Zoom indication calculée** pour inspecter la vue 3D rapprochée. Surface rose = maillage de l’indication ; lobes colorés = amplitude calculée du champ diffusé ; trait orange = repère entre sonde et centre de cible, pas une carte du champ incident.
6. Porte A : début 0, fin 20 µs, seuil relatif 0,01, gain 3. Le cas témoin donne un temps de centre voisin de 8,73 µs et une amplitude relative d’environ 0,062 (−24 dB par rapport à la référence du modèle). Ce n’est pas une amplitude étalonnée d’instrument.
7. Modifier l’orientation de la sonde par petits incréments, puis essayer +20°. Après chaque calcul, vérifier que lobes et réception changent. Le maximum mémorisé reste historique : observer l’écho courant pour comparer deux poses.
8. Recharger le témoin. Dans l’onglet 2, changer **Inclinaison normale** de MF1 de 45° à 80°, puis revenir au scan. La réception doit fortement changer : la face ne renvoie plus le même champ vers l’ouverture.
9. Recharger le témoin, puis comparer 4 et 5 MHz. Le maillage et la phase dépendent de la longueur d’onde ; le résultat n’est pas simplement recoloré.
10. Passer la porte de 0–20 à 30–40 µs. L’écho direct de MF1 sort de la sélection ; le champ monochromatique reste calculé, car la porte n’en change pas la physique.
11. Désactiver MF1 : aucun champ/écho d’indication. En préparation d’examen réel : aucun champ/signal synthétique fourni comme acquisition réelle.
12. Exporter JSON ou la scène RV : modèle, réception complexe, référence et paramètres accompagnent les données. Le champ scalaire n’est pas un critère d’acceptation industriel.

## Géométrie de l’indication

MF et fissures sont des rectangles réfléchissants. Leur centre est défini par Az/Z/profondeur. La normale est construite par

`n_defaut = cos(inclinaison) n_radiale − sin(inclinaison) f_orientation`.

La longueur suit la tangente perpendiculaire au plan d’incidence ; la largeur est dans la face. L’orientation et l’inclinaison doivent donc être définies pour le défaut réel. Une valeur par défaut de 45° est une hypothèse de test, pas une mesure d’un flanc de soudure. INC1 est une sphère réfléchissante de diamètre défini ; les contrastes acoustiques d’une inclusion réelle ne sont pas modélisés.

La partie d’une face qui sort de la paroi est écartée du calcul. La surface intégrée est affichée et peut être inférieure à la surface totale. L’accès direct est contrôlé dans la paroi principale ; la propagation dans la branche reste hors modèle.

## Calcul et échelle

Ouverture et surface sont discrétisées avec un pas nominal au plus égal à λ/3. L’onde monochromatique émise est une moyenne de sources de Green `exp(ikr)/r` sur l’ouverture équivalente, avec facteur d’obliquité. Le champ réfléchi suit une approximation scalaire de Kirchhoff sur la partie éclairée :

`P_sc(x) ≈ i k/(4π) ∫ [D_inc(y) + μ_sortie P_inc(y)] exp(ik|x−y|)/|x−y| dS`.

`D_inc` contient la pondération d’incidence de chaque source d’ouverture. La réception est la moyenne complexe du champ sur la même ouverture, avec son facteur d’obliquité. On conserve la phase jusqu’à cette intégration ; les amplitudes ne sont pas additionnées avant réception.

Le dB utilise une référence **fixe de 0,05 dans les unités du modèle** : `20 log10(|P| / 0,05)`. Ce ne sont pas des pascals ni un étalonnage DAC/TCG. La carte est affichée de −60 à 0 dB ; un résultat au-dessus de 0 dB sature la couleur, sans écrêter l’amplitude exportée. Le seuil masque seulement l’affichage. La réception est indépendante du seuil de couleur et du gain d’écran.

L’enveloppe A-scan utilise cette amplitude et un temps `2 × distance(sonde, centre) / VT`, avec une impulsion graphique de largeur fixée. Il ne s’agit pas d’un calcul de réponse impulsionnelle large bande. Les zones à moins d’une demi-longueur d’onde d’une facette ne sont pas résolues par le noyau ponctuel.

## Limites à conserver lors de l’évaluation

- Calcul scalaire, homogène, monochromatique, diffusion unique et incidence directe.
- Pas de rebonds du champ incident/diffusé sur les parois dans ce mode ; pas de skip/double-skip calculé pour les indications.
- Pas de modes élastiques L/T couplés, conversions, sabot, réfraction dans le sabot, transmission ou modèle de contact courbe.
- Approximation de face réfléchissante et de sphère éclairée ; pas de contraste d’inclusion, solution de fissure élastique, Mie, diffraction GTD ni interactions multiples entre défauts.
- Masquage à la paroi/cavité du piquage, pas de conditions aux limites élastiques complètes sur la soudure et la branche.
- Aucun calcul industriel CIVA ni validation expérimentale revendiqué. Les essais logiciels vérifient la cohérence du modèle réduit, pas la validité d’un examen réel.

## English

**Computed backscattered field — scalar** integrates complex contributions from a finite reflecting face (or illuminated sphere), excited by a finite MWB aperture. Reception averages the complex scattered pressure over the same aperture. Phase, finite-surface directivity, interference, orientation and frequency affect the result. This is a scalar Kirchhoff physical-optics approximation, not the previous magenta path or an elastic CIVA solver.

Load **Backscatter witness test — MWB 45° / 4 MHz** in tab 3 (export personal settings first). It defines a single 6 × 3 mm MF1 at azimuth −50°, Z −90 mm, depth 10 mm, normal tilt 45°. Probe starts at −50°, −100 mm, heading 0°. Wait until calculation finishes, then use **Focus computed flaw**. Gate 0–20 µs, threshold 0.01, gain 3; field cutoff −40 dB. Expected centre-path echo is about 8.73 µs, relative amplitude 0.062. Change heading, face tilt and frequency and compare the current echo, not its stored maximum.

The fixed field reference is 0.05 in model units, never renormalized per pose. Gate, screen gain and colour threshold do not change the solved harmonic field. While a new pose is computed, old field data is hidden and point recording is disabled. The worker preserves smooth manual movement.

Important limits: direct illumination and single scattering only; no wall-bounce scattering, elastic modes/conversion, wedge/contact, full weld propagation or broadband impulse response. Root/cap heuristic echoes are excluded from this scalar A-scan. The time-of-flight uses the surface centre path. Surface orientation is user-defined and must not be mistaken for a measured bevel orientation. No industrial or experimental validation is claimed. This release is for the user's technical review; no evaluation emails have been sent.
