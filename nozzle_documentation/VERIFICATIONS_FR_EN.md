# Vérifications — Nozzle REV0.5 MWB / PA32

- Réception MWB témoin inchangée : temps ≈8,729713µs, amplitude relative ≈0,0619371. Contrôles de sensibilité à l’orientation, normale et fréquence, fraîcheur des données et fonctionnement en iframe : PASS.
- PA :32 éléments réels dans la quadrature, pitch0,5mm, span entre centres15,5mm. Réception réciproque comparée à une intégration indépendante sur l’ouverture pour les cas uniforme et phasé : PASS.
- Champ incident PA et pression incidente aux points de la surface cohérents ; champs incident/diffusé et réception issus des mêmes phases : PASS.
- Secteur35–70°,19 angles au pas2° avec70° inclus ; A-scan sélectionné, S-scan direct et B-scan des points enregistrés ; données PA dans les exports : PASS.
- Témoin PA : temps ≈8,729713µs, amplitude relative ≈0,00537995 à45° ; forte variation à65°. Ces amplitudes de modèle ne sont pas des étalons d’instrument.
- Mode préparation sans acquisition réelle : suppression des signaux synthétiques comme mesures réelles : PASS.
- Geste MWB, saisie sans saut, raster/inversion, butées, relâchement hors canevas, caméra et export : PASS.
- Streamlit réel local : boutons PDF FR/EN, fichiers identiques, points conservés lors du téléchargement ; méthode et session PA conservées au passage FR→EN ; rapport HTML échappé : PASS.
- Manuels :13 chapitres et14 captures réelles dans chaque langue ; cas témoin chiffré identique FR/EN, PDF/HTML autonomes et liens internes : PASS.

These are software and reduced-model checks, not experimental validation or CIVA equivalence. The scalar model does not solve wedge propagation, curved contact, coupled elastic waves or wall-bounce scattering. Reference0.05 and dB colours are model units, not instrument calibration. Camera tracking/input still requires Fabien’s adapter.
