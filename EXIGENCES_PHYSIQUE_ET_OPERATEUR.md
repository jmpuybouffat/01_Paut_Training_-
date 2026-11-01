# Exigences du twin nozzle — mise au point avec l’utilisateur

L’opérateur balaie la surface extérieure avec un palpeur monoélément. Le geste opérateur doit se faire sur la pièce 3D ; le déroulé est un outil secondaire. La position, l’orientation et le faisceau/rayon doivent être synchronisés entre toutes les vues. La caméra ne doit pas déplacer le palpeur. L’apprenant recherche les indications sans voir leurs positions ou types ; la révélation appartient au mode instructeur.

## État au présent correctif

Déplacement du symbole MWB sur la surface cylindrique principale par intersection analytique du rayon de souris avec le cylindre. Position radiale contrainte ; déplacement à l’intérieur des limites du plan ; exclusions et ouverture bloquent le geste. Le palpeur reste symbolique : contact exact du sabot, balayage sur la branche et collision de son volume non implémentés. Rafraîchissement par requestAnimationFrame. Le déroulé reste sélectionnable. Indications masquées par défaut, et absentes de la vue de surface même quand l’instructeur révèle les vues internes.

Le modèle acoustique demandé n’est pas implémenté. Les rayons géométriques et les amplitudes heuristiques existants ne sont pas un substitut à ces moteurs.

## Rôles physiques attendus

- Green : propagation issue d’une ouverture finie, avec phase et dépendance fréquentielle. En acier, le problème visé doit traiter les ondes élastiques et leurs polarisations, pas présenter un Green acoustique scalaire libre comme une solution élastodynamique complète.
- Born : approximation de diffusion volumique, adaptée sous hypothèse de faible contraste ; une inclusion exige ses propriétés et le contraste avec le matériau de base.
- Kirchhoff : approximation de la diffusion/réflexion sur des surfaces, avec géométrie, normales, incidence et domaine de validité explicités.
- GTD (ou formulation uniforme adaptée) : diffraction aux bords ; nécessite les géométries de bord, coins, conditions aux limites et le traitement des zones de transition/ombre.

Il ne s’agit pas de quatre variantes graphiques d’un même éventail de rayons. Ils doivent être couplés ou sélectionnés suivant le phénomène et les hypothèses.

## Données physiques encore nécessaires

Dimensions et géométrie actives du cristal, géométrie/propriétés du sabot, impulsion et bande passante, couplage, propriétés élastiques/atténuation des pièces, définition physique de l’inclusion et des défauts plans, préparation et soudure volumique. Les 5 indications ont leurs dimensions de base, mais leurs poses et leur relation aux flancs doivent être fixées pour chaque pièce.

## Vérification attendue avant de présenter un moteur comme opérationnel

Vérifier directivité et champ proche/lointain de la source, temps de vol analytiques, interfaces et conversions de modes, réponses de référence pour inclusion et réflecteur plan, diffraction de bord et stabilité aux frontières, convergence numérique, dépendance à la fréquence, comparaison à des mesures ou à un moteur de référence. Distinguer calcul numérique, validation analytique et comparaison expérimentale.

Cascade/CAD-TCG restent des modules distincts. La classification ne peut être déduite automatiquement de la nature connue du défaut injecté dans l’exercice. Aucun moteur Green/Born/Kirchhoff/GTD opérationnel ou validé n’est revendiqué dans ce correctif d’interface.
