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
