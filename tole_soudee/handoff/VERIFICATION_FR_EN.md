# Vérifications P03 / P03 checks

Vérifié le 5 novembre 2026 / Checked 5 November 2026.

- Tests numériques Node : limites du sabot, rayon 45°, émission/réception SE distinctes, temps de parcours analytiques directs et de fond, volume de sphère, proportionnalité au contraste de Born, absence d’interface ZAT artificielle, rétroprojection SE corrigée de l’écartement, valeurs PA et champs finis. PASS.
- Tests navigateur Chromium : SE/MWB/PA, drapeaux et conservation des valeurs FR/EN, suspension hors contact, créneaux alternés de 2 mm, arrêt sans ajout tardif, vues et exports, séparation des informations de vérité du mode examen. PASS.
- Interface caméra : pose calibrée acceptée, confiance trop faible et levée refusées, export de pose 6D. PASS.
- Streamlit local séparé : chargement de plate_app.py, calcul dans l’iframe et commutation FR/EN. PASS.
- La géométrie STEP n’a pas été modifiée par P03 ; les contrôles CAO de la livraison précédente restent applicables. Les métadonnées matériaux et sondes ont été mises à jour.

These are software/kinematic checks, not validation against CIVA, laboratory specimens or certified hardware. Amplitudes, detection performance, sector coverage through a real wedge and certification criteria are not validated by these tests.

Ces contrôles logiciels ne valident pas les amplitudes, les performances de détection, la couverture réelle à travers le sabot ni une procédure de certification. Aucune comparaison CIVA ou mesure de laboratoire n’est revendiquée.

P03 : tests de vrais événements souris (glissement X/Y et capture du pointeur), relâchement avec recalcul du champ, boutons Y, flèches clavier, zoom bilingue, butée sans traversée du bourrelet et profil de préparation en X. PASS. Aire du contour de sabot non croisé vérifiée numériquement. Le STEP n’a pas été modifié. / Actual pointer dragging, release field refresh, Y controls, keyboard, bilingual zoom, weld stops and explicit X profile pass; footprint area is checked independently.

P03 : tests de conservation des plages d’axes et de la caméra après Y−1, X+1, X−1 et recalcul complet ; remise à zéro volontaire ; palette et référence fixes communes ; rayons sur les deux cartes ; profondeur 0 sur la face de palpage. PASS. Tests physiques : champ diffusé nul sans défaut, sommation cohérente des contributions et image scalaire sur la face opposée. / Zoom/camera retention, 1 mm steps, intentional reset, shared field palette/reference, rays and depth convention pass; zero scattering without flaws and scalar opposite-wall image are checked.

P03 : aperçu de champ pendant un vrai glissement de souris (11 lignes en profondeur), puis grille affinée au relâchement (21 lignes), sans changement de référence d’amplitude. PASS. / Live coarse physical-field preview and refined release grid verified under actual pointer events.

Documentation P03 édition1 : captures réelles FR/EN, 13 chapitres et 10 illustrations par langue, exercices MWB témoin et créneau12 poses vérifiés. PDF/HTML autonomes et liens internes contrôlés. Streamlit : les deux PDF téléchargés sont identiques aux fichiers publiés et ne réinitialisent pas l’acquisition. PASS. / Edition1 documentation: offline illustrated manuals and checked exercise values; both Streamlit PDF downloads preserve acquisition state.
