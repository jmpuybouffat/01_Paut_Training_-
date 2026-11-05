# Vérifications P01 / P01 checks

Vérifié le 5 novembre 2026 / Checked 5 November 2026.

- Tests numériques Node : limites du sabot, rayon 45°, émission/réception SE distinctes, temps de parcours analytiques directs et de fond, volume de sphère, proportionnalité au contraste de Born, absence d’interface ZAT artificielle, rétroprojection SE corrigée de l’écartement, valeurs PA et champs finis. PASS.
- Tests navigateur Chromium : SE/MWB/PA, drapeaux et conservation des valeurs FR/EN, suspension hors contact, créneaux alternés de 2 mm, arrêt sans ajout tardif, vues et exports, séparation des informations de vérité du mode examen. PASS.
- Interface caméra : pose calibrée acceptée, confiance trop faible et levée refusées, export de pose 6D. PASS.
- Streamlit local séparé : chargement de plate_app.py, calcul dans l’iframe et commutation FR/EN. PASS.
- La géométrie STEP n’a pas été modifiée par P01 ; les contrôles CAO de la livraison précédente restent applicables. Les métadonnées matériaux et sondes ont été mises à jour.

These are software/kinematic checks, not validation against CIVA, laboratory specimens or certified hardware. Amplitudes, detection performance, sector coverage through a real wedge and certification criteria are not validated by these tests.

Ces contrôles logiciels ne valident pas les amplitudes, les performances de détection, la couverture réelle à travers le sabot ni une procédure de certification. Aucune comparaison CIVA ou mesure de laboratoire n’est revendiquée.
