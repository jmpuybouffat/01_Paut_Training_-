# Interface Fabien — caméra PC ou externe, sans casque / PC or external camera, no headset

## Livré / Supplied

- CAO STEP et maillages JSON dans CAO ; géométrie de vérité séparée des réponses d’acquisition.
- Application autonome et sources, calcul dans un Web Worker.
- Entrée JavaScript **window.ByteNDTPlate.applyTrackedPose(pose)**, asynchrone.
- Événement **byte-ndt-plate-response** pour une acquisition acceptée ; détail = copie exportable du dernier enregistrement, sans vérité dans le mode examen.
- Session exportée : propriétés nominales, profils de sonde, poses de contact, angles, événements acoustiques, limites de contact et rapport.

Supplied: STEP/JSON CAD, standalone app and source, worker calculations, asynchronous pose input, response event and session export. Video tracking is not supplied. No headset is assumed or required.

## Repère / Frame

Repère direct, origine coin inférieur de tôle : X longitudinal [0,245], Y transversal [0,250], Z vers le haut [0,10], axe soudure Y125. Unités mm ; pour un client en mètres, multiplier toutes les positions par 0,001. Ne pas appliquer directement les angles de caméra sans calibrer son repère.

Right-handed plate frame: X along weld, Y across weld, Z up. Millimetres, with explicit 0.001 conversion to metres. Camera extrinsics and handedness conversions must be calibrated externally. No automatic axis swap or recentering is performed.

## Entrée / Input

```javascript
// Activer « Caméra Fabien » dans le panneau de liaison.
const result = await window.ByteNDTPlate.applyTrackedPose({
  sequence: 1,               // croissant / strictly increasing
  timestamp_ms: 0,           // horloge du suivi / tracker clock
  position_mm: [105,111,10], // point d'émergence, déjà en repère tôle
  euler_xyz_deg: [0,0,90],   // R = Rz Ry Rx, degrés / degrees
  face: 'TOP',              // ou / or BOTTOM
  confidence: 0.95
});
// {accepted:true, reason:'CONTACT'} ou un motif de refus / rejection
window.addEventListener('byte-ndt-plate-response', event => {
  const acquisition = event.detail;
  // copier / transmettre les données ici ; pas de serveur imposé
});
```

La pose est celle du **point d’émergence à la surface acier**, pas celle du centre du boîtier ou du marqueur vidéo. La transformation rigide marqueur → émergence doit être fournie par l’intégrateur. Le sabot réel et son décalage devront remplacer les valeurs provisoires.

Input is the steel-interface emergence point, not the marker/probe-body centre. The integrator must supply the marker-to-emergence rigid transform and actual wedge dimensions.

TOP : position Z10, Euler [0,0,cap]. BOTTOM : Z0, Euler [180,0,cap]. Les rotations suivent Rz Ry Rx. P02 accepte une tolérance de 0,5 mm en Z et 3° autour de la pose de contact ; la pose acoustique est ensuite contrainte au plan de contact. Une vraie simulation de couplage partiel ou de sonde inclinée n’est pas implémentée.

Rejects: source caméra non activée, créneaux en cours, séquence ancienne, confiance <0,7, données invalides, levée/inclinaison excessive, bord de tôle ou bourrelet. Les horodatages sont conservés par l’appelant ; la numérotation protège contre les doublons. Fabien doit gérer les pertes de suivi et les délais de transmission. Appeler séquentiellement en attendant la promesse ; les anciens calculs sont annulés quand une pose plus récente arrive. P02 calcule sur demande, pas à une cadence vidéo garantie.

Rejected inputs include disabled camera source, raster running, stale sequence, confidence below 0.7, invalid values, lift/tilt or geometric collision. Acoustic contact is planar; no partial-coupling solver. Await each promise for sequential acquisition. New poses cancel older calculations; no guaranteed video frame rate.

## À raccorder avec Fabien / Integration work

Choix caméra, suivi d’un marqueur ou du traducteur, calibration image/repère tôle, transformation marqueur/émergence, gestion perte de suivi, ressenti visuel du contact et essais de précision. L’interface ne lit aucun flux vidéo et ne demande aucune autorisation caméra. L’utilisateur ouvre l’application et réalise ses exercices ; l’adaptateur de suivi est une tâche d’intégration.

Camera choice, marker/probe tracking, camera/plate calibration, marker offset, tracking-loss handling and accuracy testing remain the integrator’s work. The app does not access video. This is a reviewable interface, not a finished camera-training system.

## Acoustique et validation / Acoustics and validation

Voir les notices FR/EN : modèle scalaire réduit, amplitudes non étalonnées, sabot non propagé, S-scan/cumul par rétroprojection. Les trois angles, dimensions et positions du scénario sont modifiables via JSON ; les domaines ML non validés ne sont pas générés automatiquement. Séparer les jeux ML par scénario/pièce pour éviter la fuite des mêmes géométries entre entraînement et évaluation.

Reduced scalar acoustics; no industrial qualification or secure examination platform. Preserve scenario lineage and split ML datasets by specimen/scenario.
