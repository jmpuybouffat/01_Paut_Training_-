# Protocole court d’évaluation / Short evaluation protocol

Ces essais évaluent le fonctionnement du prototype et sa lisibilité pédagogique. Ils ne qualifient pas une procédure de contrôle.

## Français — limites et faisceau pendant le scan

1. Lancer le paquet complet, choisir FR, Formation puis Démo de balayage en paroi. Ouvrir 3 · Scan manuel. Laisser Instructeur décoché.
2. Garder la MWB 45° / 4 MHz pour le premier essai. Saisir le symbole de sonde sur la surface 3D et balayer lentement. Vérifier que le champ coloré, la coupe et l’A-scan suivent la même pose.
3. Approcher le piquage. Vérifier l’arrêt de l’enveloppe du sabot avant la zone interdite et lire le motif affiché. Le sabot est une approximation rectangulaire centrée, pas une collision CAO complète.
4. Réinitialiser, lancer Créneaux, puis vérifier l’arrêt à une limite géométrique. Inverser le parcours et relancer. Vérifier que le sens change sans modifier l’orientation du palpeur.
5. Cliquer dans la vue opérateur puis tester STOP/Pause, Espace et Échap. Vérifier l’arrêt et le relâchement de la souris.
6. Garder Champ avec réflexions — premier modèle. Pendant le geste, observer le champ en dB et les trajets réfléchis. L’échelle reste fixe relativement au palpeur pour un angle et une épaisseur donnés.
7. Comparer, si utile, Volume 3D calculé et Coupe calculée : ce sont des champs directs scalaires réduits. Ne pas les confondre avec une simulation élastodynamique complète ou un A-scan calculé à partir de ce champ.
8. Changer FR → EN → FR. Vérifier les boutons, les motifs d’arrêt, les types/emplacements et les en-têtes du tableau. Dimensions, positions et exclusions doivent être conservées.
9. Après l’essai aveugle, activer Instructeur pour comparer les références. Les cibles sont artificielles et situées dans la paroi principale ; le placement réel sur flancs reste à définir.
10. Exporter le scan et, pour l’intégration, la scène RV. Noter les incohérences avec une capture et la pose/les réglages associés.

Retour souhaité : 3 points convaincants, 3 corrections prioritaires, puis les données ou essais nécessaires à l’étape suivante. Les versions examinées doivent être identifiées par le nom du paquet et la révision GitHub.

## English — scan limits and field visualization

1. Launch the full package, select EN, Training and Main-wall scan demo. Open 3 · Manual scan; keep Instructor unchecked.
2. Use MWB 45° / 4 MHz initially. Drag the probe on the 3D surface and check that the coloured field, section and A-scan use the same pose.
3. Approach the nozzle and read the geometric stop reason. Footprint checking is a centered rectangular approximation, not complete CAD collision.
4. Reset, run Raster and verify the geometric stop. Reverse scan and resume; probe orientation should remain unchanged.
5. Activate the operator panel and test STOP/Pause, Space and Escape. Check that motion stops and mouse capture releases.
6. Use Reflected field — first teaching model. Observe the dB map and reflected paths during motion. The relative display scale remains fixed for a given angle and thickness.
7. Optionally compare Computed 3D volume and Computed cut. These are reduced scalar direct-field calculations, not a complete elastic model or a physically coupled A-scan.
8. Switch FR → EN → FR and check control labels, stop reasons, indication types/locations and table headers. Dimensions, positions and exclusions must remain unchanged.
9. After the blind exercise, reveal Instructor references. Targets are artificial main-wall placements, not real bevel-face flaws.
10. Export scan/VR data and report issues with a screenshot and the associated settings/pose.

Requested feedback: 3 useful aspects, 3 priority corrections, and the data/tests needed for the next stage. Record the package name and GitHub revision used.
