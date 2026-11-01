## Affichage de formation restauré

Le mode par défaut **Champ avec réflexions — premier modèle** reprend l’accumulation pédagogique d’énergie sur un éventail de rayons dans l’acier, pondérée par une divergence, une atténuation et un facteur de rebond illustratifs. Échelle 0 à −40 dB, carte colorée et enveloppe 3D, synchronisées au même palpeur. Ce mode conserve le comportement visuel du premier twin ; il ne revendique pas un champ élastique calculé.

Les deux modes **Volume 3D calculé** et **Coupe calculée** utilisent le modèle réduit ci-dessous. Le volume est évalué sur une grille S/T/U par la même intégrale complexe, et non obtenu en tournant une coupe 2D. L’affichage sélectionne les points au-dessus du seuil dB et masque les points hors matière ou après la première interface. Les réflexions ne sont donc pas ajoutées comme des champs scalaires calculés dans ces deux modes.

# Carte de champ direct — modèle scalaire équivalent

Il s’agit d’un calcul numérique de champ monochromatique scalaire, pas d’un moteur CIVA ou d’un champ élastique complet.

Une ouverture rectangulaire uniforme 8 × 9 mm, normale à l’axe du faisceau équivalent, est intégrée par quadrature. À chaque point, le noyau utilisé est G(r) = exp(i k r)/(4πr), avec k = 2πf/c. Les contributions complexes sont additionnées avant de prendre le module. Le calcul inclut donc les interférences spatiales, la phase et la fréquence ; il ne dessine pas une gaussienne arbitraire.

La vitesse est la valeur VT saisie dans l’application. Pour une onde T dans l’acier, le scalaire affiché est seulement un substitut d’amplitude de déplacement : ce n’est pas une pression acoustique, ni un vecteur de déplacement élastique résolu avec ses polarisations.

La carte utilise 20 log10(|u|/max_grille|u|), avec une plage de couleur 0 à −40 dB. La normalisation est propre à chaque grille/fréquence : comparer les formes est possible, comparer ces couleurs comme des amplitudes absolues étalonnées ne l’est pas.

L’ouverture équivalente est placée au point d’entrée et orientée suivant l’angle nominal dans la pièce. Les dimensions sont reprises comme ouverture équivalente ; le transfert depuis le cristal via le sabot, la réfraction, les coefficients de transmission, le couplage, la courbure de contact et la bande passante ne sont pas calculés.

Les pixels sont masqués hors de la paroi principale et après la première interface rencontrée par le rayon central. La carte ne représente que le champ direct ; les trajets réfléchis restent des rayons géométriques. Une coupe colorée du champ est aussi projetée sur la vue 3D, sans prétendre à un volume de champ élastique complet.

L’A-scan reste généré par les heuristiques de géométrie/indications. Il n’est pas calculé à partir de ce champ. Born, Kirchhoff et GTD ne sont pas ajoutés par cette étape. Le menu des modèles de diffusion futurs reste distinct du champ direct scalaire effectivement calculé.

Tests : symétrie de l’ouverture, normalisation, changement du motif avec la fréquence, comparaison de directivité en champ lointain à la forme sinc d’une ouverture rectangulaire dans le même modèle scalaire. Ces tests vérifient ce calcul réduit ; ils ne valident pas un examen industriel ni l’équivalence avec CIVA.
