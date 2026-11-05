# BYTE NDT — cadre commun de formation / Common training framework — V1

Cette référence fixe le socle de convergence des modules. Nozzle REV0.5 est le
jalon MWB/PA ; la tôle P03 reste une application distincte. Les implémentations
Canvas/Plotly et les repères géométriques peuvent différer ; les conventions
opérateur et la provenance des données doivent être explicites.

This reference defines the shared training baseline. Nozzle REV0.5 is the MWB/PA
milestone; plate P03 remains separate. Renderers and geometric frames may differ;
operator conventions and data provenance must remain explicit.

## Parcours commun / Common workflow

1. **Pièce / Specimen** — identification, dimensions, repère et accès.
2. **Réglages / Setup** — sonde, méthode, vitesse, angles, limites et scénario.
3. **Palpage / Scanning** — geste, orientation, contact/butées, vues synchronisées.
4. **Procédure et bilan / Procedure and review** — observations, rapport, exports,
   manuels FR/EN et dossier caméra de Fabien.

## Conventions opérateur / Operator conventions

- Langues 🇫🇷/🇬🇧, paramètres numériques canoniques inchangés.
- Gain d’affichage **en dB**, distinct de la référence de champ ; couleurs communes
  bleu/cyan/vert/jaune/orange/rouge, légende et référence obligatoires.
- Temps en µs, positions en mm, angles en degrés. Profondeur et coordonnées
  mondiales sont distinguées ; les axes restent adaptés à la pièce.
- Calcul courant, attente, butée, absence de données et préparation sans acquisition
  réelle sont identifiés. Ne pas afficher un ancien champ comme une nouvelle pose.
- Déplacement, rotation de sonde et caméra sont des actions distinctes.
- Retour calculé et simple rayon pédagogique sont distingués ; A-scan issu du
  calcul de réception lorsque ce mode est sélectionné.
- Préparation d’examen ≠ acquisition instrumentale ou qualification de procédure.

Same principles apply in English: canonical values, dB gain, common field palette
with units/reference, explicit frames, data freshness, separate probe/camera
motion and a clear distinction between explanation and instrument acquisition.

## Reproductibilité / Reproducibility

Un cas témoin donne géométrie, matériau, sonde, pose, méthode, modèle, angles,
porte, gain et résultats attendus. La configuration et les échos doivent être
exportables. Pour Nozzle : MWB45°/4MHz et PA32/5MHz, MF1 Az−50°, Z−90, profondeur10,
sonde Az−50°, Z−100, orientation0°. Temps de centre ≈8,729713µs ; amplitudes du
modèle différentes selon les ouvertures/phases, sans valeur d’étalonnage.

Nozzle enregistre le gain dB, la langue d’acquisition, les portes, le profil,
les angles/événements PA et les temps du navigateur aux points enregistrés.
Les traces conservent leur angle sélectionné ; ces temps ne définissent pas une
vitesse physique étalonnée. Les seuils d’affichage ne doivent pas modifier la
réception calculée. La langue conserve la session locale de l’onglet ; une autre
configuration utilise une session distincte. L’export reste la trace de référence.

Witness settings and model identifiers accompany data. Display normalization is
not an instrument calibration. Repeated calculations at fixed settings must give
consistent numerical results. Browser times describe software interaction, not
calibrated encoder motion.

## Interfaces Fabien / Fabien integration

Repère direct, unités explicites, point d’émergence, orientation et normale de
surface ; conversion mm→m =0,001 ; rotations transformées avec la géométrie.
Caméra PC/externe sans casque. Détection vidéo, calibration marqueur/émergence,
qualité du suivi et gestion de perte de contact restent des éléments d’intégration.

Les interfaces existantes sont spécifiques : Nozzle expose `BYTE_NDT.getPose`,
`getScene`, `getBeamRays` et les exports de scène ; la tôle expose une entrée
`ByteNDTPlate.applyTrackedPose`. Un adaptateur commun doit respecter ces contrats,
pas assimiler automatiquement les deux repères. Aucun client caméra achevé n’est
revendiqué par la seule fourniture de ces interfaces.

## Revue avant diffusion / Release review

Vérifier langue, unités, témoin, geste/butées, cohérence champ/A-scan, profils PA,
portes, exports, rapport et PDF. Documenter ce qui est heuristique, scalaire ou
non raccordé. Retours Fabien pour la caméra, Jacques Marlier pour les exercices,
la lisibilité et les exigences du parcours de formation/examen. La comparaison
expérimentale/CIVA et la validation de procédure restent distinctes des tests
logiciels.
