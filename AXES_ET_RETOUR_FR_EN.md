# Scan manuel monoélément — axes et retour / Single-element manual scan

## Français

Dans Scan manuel, choisir **Trajectoire** :
- **Libre** : déplacement sur la paroi du tube principal. Molette, ±1° ou Orientation locale pour orienter la sonde. En Libre, la valeur est l’angle de la sonde par rapport à l’axe longitudinal local du tube.
- **Axe tube principal** : déplacement circonférentiel à Z constant ; orientation locale réglable.
- **Axe piquage** : suivi sur le tube principal du contour d’intersection avec une enveloppe coaxiale au piquage. La sonde vise le contour de soudure ; Orientation locale ajoute un écart manuel à cette direction. Recul soudure modifie le rayon de cette enveloppe : il ne représente pas une distance géodésique constante à la soudure. Parcours ± avance autour du piquage. La sonde ne passe pas sur la branche et ne quitte pas la paroi principale.

Le plan défini dans Réglages et les encombrements restent prioritaires. Un plan restreint peut empêcher de faire le tour : élargir ses bornes selon la zone de travail prévue. Une géométrie ne permettant pas un contour complet est signalée. Le raccord depuis la position actuelle est vérifié et peut s’arrêter avant le contour. Le bouton Créneaux reste réservé au mode Libre.

La coupe est une projection Z/profondeur des rayons 3D : elle peut écraser un trajet circonférentiel. La vue 3D permet de l’examiner. Glisser horizontalement dans la coupe ou le champ déplace la sonde selon sa direction locale ; la molette l’oriente. En 3D, le glissement de la vue filaire reste une commande caméra.

**Retour indication pédagogique** affiche en magenta le trajet réciproque du plus fort écho d’indication courant dans la porte active (pas le maximum mémorisé). Le temps et l’amplitude proviennent du même événement heuristique que l’A-scan. Ce tracé suit en sens inverse le préfixe du rayon jusqu’au point d’approche de la cible : il illustre la rétrodiffusion, sans résoudre une réflexion spéculaire sur la surface réelle du défaut, ni son champ diffusé. Il n’est disponible qu’en formation. L’activer peut aider à localiser la cible ; le laisser désactivé pour un exercice aveugle. Aucun couplage physique Green/Kirchhoff/GTD n’est revendiqué.

**Pièce personnalisée** désigne la géométrie et les indications à renseigner, indépendamment du mode de geste.

## English

Choose **Path** in Manual scan: Free for wall motion and manual heading, Main pipe axis for a constant-Z circle, or Nozzle axis for a main-wall contour coaxial with the branch. Nozzle mode aims the probe at the weld contour; Local skew adds manual adjustment. Weld stand-off enlarges the coaxial envelope, rather than prescribing an exact surface distance. Path ± advances along the contour. Contact remains on the main pipe, subject to plan boundaries, excluded zones and approximate footprint clearance. Raster playback uses Free mode.

The section remains a Z/radial-depth projection and may compress circumferential paths; use the 3D view to inspect those. Drag horizontally in section/field to move the same probe and use the wheel for heading. Wireframe 3D dragging controls its camera.

Teaching flaw return shows the strongest CURRENT flaw echo inside the active gate, using the same heuristic amplitude/time as the A-scan. Magenta arrows follow the incident ray prefix in reverse from its closest target approach. This illustrates reciprocal backscatter, not a solved specular flaw reflection or scattered acoustic field. Training only; leave off for blind exercises. Custom specimen means user-defined geometry and flaws, not a motion mode.
