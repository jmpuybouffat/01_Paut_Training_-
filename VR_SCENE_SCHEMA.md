# BYTE_NDT_VR_SCENE_V1 — interface pour reprise en réalité virtuelle

Le bouton **Exporter scène RV** produit `NOZZLE_VR_SCENE_V1.json`. Aucun envoi à un tiers n’est effectué. Les données décrivent une scène géométrique et des réponses pédagogiques non étalonnées, pas un modèle acoustique validé.

## Repère commun

Repère direct, longueurs en mm, angles en degrés. Axe du tube principal : Z. Azimut 0° : +X ; azimut positif : +X vers +Y. Origine au centre géométrique du tube principal.

Pour un moteur RV travaillant en mètres, diviser toutes les positions et dimensions par 1000. La conversion vers un repère moteur différent doit être appliquée à la géométrie, aux positions ET aux rotations.

## Pose du palpeur

`current_pose.position_mm` : point de surface du tube principal. `rotation_matrix_local_to_world` : matrice 3×3, vecteurs de base en COLONNES, multiplication sur vecteurs colonnes. Axes locaux : X = direction tangentielle avant, Y = direction latérale, Z = normale extérieure. La matrice est orthonormale et de déterminant +1.

`beam_direction_world` : vecteur unitaire du rayon central dirigé dans la matière. `local_axes` fournit aussi les trois vecteurs séparément. Les angles `azimuth_deg`, `heading_deg` et la coordonnée `z_mm` sont conservés pour l’édition. `scan_status` ne constitue pas une certification d’accès.

## Scène et animation

- `specimen` et `joint` : dimensions paramétriques du nozzle et du joint approché.
- `probe` : configuration MWB, données nominales et source de vérification catalogue.
- `beam.segments_world_mm` : segments de rayons géométriques, rebonds et parcours cumulés. `validated_physics` vaut false.
- `trace` : liste ordonnée des poses du point de sonde ; aucune vitesse de déplacement physique n’est imposée par cette version.
- `samples` : points enregistrés, portes A/B/C, réponses pédagogiques et segments de rayons.
- `indications` : données du scénario, incluant les positions connues de l’auteur. Le fichier de scène destiné à l’auteur n’est pas une épreuve aveugle sécurisée. Ne pas le remettre comme corrigé à l’élève.
- `training_signal_model` : `UNCALIBRATED_HEURISTIC`.

Dans le document HTML, l’API locale `window.BYTE_NDT.getPose()`, `.getScene()` et `.getBeamRays()` permet à un intégrateur de lire l’état courant. Elle ne crée pas une session WebXR, ne diffuse pas de données réseau et ne remplace pas un moteur RV.

## Géométrie et limites

L’intégrateur reconstruit les cylindres et le repère de branche à partir des paramètres. Le modèle n’exporte pas de solide CAO booléen, de maillage de soudure validé ou de scène glTF complète. Les parcours sont calculés dans la paroi principale ; la propagation complète dans la branche et la soudure reste à développer.

## Arrêts de mouvement

`motion_limits` décrit le modèle d’enveloppe centrée et les événements d’arrêt. `stop_events` contient les motifs, l’azimut, Z, l’orientation et le temps écoulé du document. L’événement local `BYTE_NDT_MOTION_STOP` est émis à l’arrêt opérateur ou à la rencontre d’une limite. Cette interface sert à reprendre le comportement dans un moteur RV ; elle ne constitue pas un interverrouillage matériel ou une collision CAO complète.

## Computed scalar backscatter extension — RÉTRO SCALAIRE

When `beam.field_view == "scattered"`, `scalar_scattering` contains:

- `model`, `scope`, `validated_elastic: false`;
- `computation_pending`: do not render an old field or treat an empty pending array as a physical null;
- `pose`: the pose associated with the computed field;
- `reference_amplitude: 0.05` in arbitrary model units;
- `field_samples_world`: `{p: [x,y,z], db}` points, positions in mm in the same world frame as the specimen;
- `section`: selected-flaw section grid (`lo`, `hi`, azimuth, `nx`, `ny`, cells containing world position, dB and phase in radians);
- `targets`: IDs, finite surface quadrature points/normals/areas, received complex amplitude, illuminated area;
- `events`: relative scalar amplitude, phase and centre-path time in µs.

The outgoing field is scalar direct-path single scattering without wall bounces. The JSON contains data for a VR client; it is not itself an immersive/WebXR application. Existing geometric ray segments are explicitly labelled as references, not sampled scattered-field paths. The existing right-handed frame and mm-to-metre conversion for a VR client remain unchanged.

## REV0.5 — PA32 / 32-element PA

`acquisition` identifies `PHASED_ARRAY_32` or `MONO_ELEMENT`. Existing pose matrices,
world frame and units are unchanged. For PA, the top-level `pa` block contains the
32-element 5 MHz profile, sector events, `incident_field` grid and direct-ray
`backprojection`. Recorded points contain `pa_profile` and `pa_sector`.

Both PA incident and scattered fields use element phases and the same equivalent
steel-interface aperture. Scattered reception is coherent over all active
aperture points; `scalar_scattering.model` is
`SCALAR_PHASED_ARRAY_KIRCHHOFF_SINGLE_SCATTERING`. The scalar field remains direct,
not a solved wall-bounce or elastic wedge model. Source-element width0.45mm,
pitch0.5mm, elevation12mm and the focus are model parameters, not approved
instrument focal laws. Do not upload these values as hardware laws.

PA S-scan uses direct time/angle backprojection into longitudinal Z/radial depth.
Its B-scan uses the first35° ray at recorded points; selected-ray A-scan can use a
different angle. These views do not reveal exact flaw geometry or establish
volumetric coverage. In real-examination preparation, no synthetic acquisition
is supplied as a real instrument measurement.

For Fabien: no headset is required or assumed. The exported scene and local
`getPose/getScene/getBeamRays` APIs are readers; camera tracking, calibrated pose
input and tracking-loss/contact handling still require an adapter. This differs
from the plate’s separate `ByteNDTPlate.applyTrackedPose` entry point.
