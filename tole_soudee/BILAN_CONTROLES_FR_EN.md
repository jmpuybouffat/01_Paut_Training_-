# Vérifications CAO / CAD checks — 4 novembre / November 2026

## Français

Sept tests géométriques réussis avec CadQuery/OpenCascade :

1. Neuf solides valides et dimensions de référence respectées.
2. Quatre faces de chanfrein à 45°.
3. Partition de la tôle sans chevauchement volumique ; volume hors bourrelets = 612 500 mm³.
4. Bourrelets lisses conformes à l’aire analytique du segment circulaire ; rayon 17,45 mm, Z extrêmes −2,5 et 12,5 mm.
5. Variantes de talon 1 et 1,5 mm régénérées ; paramètres incompatibles rejetés.
6. Références d’indications aux dimensions prévues : faces de collage sur les chanfreins, sphères de diamètre 0,5 mm, fissure dentelée d’encombrement 2 × 0,5 mm. Pas de vide d’ouverture inventée.
7. Réimport des STEP FR et EN : neuf solides valides, même volume, dimensions globales 245 × 250 × 15 mm bourrelets compris. Les stries retirent une petite quantité de matière sous l’enveloppe nominale, sans dépasser les hauteurs maximales.

Volume total détaillé : environ 627 396,63 mm³. Contrôle navigateur réussi : vues 3D, drapeaux FR/EN, textes et tableau d’indications traduits, commandes de visibilité et zoom sur la soudure. La visionneuse inclut ses ressources pour une ouverture locale sans connexion.

L’import dans Autodesk Fusion n’a pas été exécuté dans cet environnement. La vérification de la pièce réelle, de sa métallurgie et des caractéristiques acoustiques reste distincte. Aucun résultat ultrasonore n’est revendiqué par cette livraison CAO.

## English

Seven CadQuery/OpenCascade geometry tests passed: valid nine-solid assembly; four 45° bevel faces; non-overlapping plate partition; analytic circular caps; land variants; finite flaw reference dimensions and bevel alignment; French/English STEP re-import with identical volume and global dimensions.

Plate material volume excluding reinforcements is 612,500 mm³. Detailed total volume is approximately 627,396.63 mm³. Reinforcements reach Z = −2.5 and 12.5 mm. Browser checks passed for 3D rendering, FR/EN flags and labels, translated flaw table, visibility controls and weld focus. The viewer is self-contained for offline use.

Autodesk Fusion import has not been executed here. No ultrasonic field, signal or industrial examination validation is claimed by this CAD release. Proposed groove details and flaw locations require review; air opening and acoustic properties remain pending.
