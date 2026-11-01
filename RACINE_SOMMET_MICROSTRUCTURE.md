# Profils irréguliers et description de microstructure

## Racine et sommet facettés

Dans la barre latérale, sous Préparation du joint, ouvrir **Racine et sommet — profils facettés de formation**. Profils irréguliers activés par défaut ; hypothèses initiales : 0,8 mm à la racine, 1 mm au sommet, 24 facettes, identifiant 17. Ces valeurs ne sont pas des mesures de soudure et restent modifiables.

Les maillages sont déterministes : un même identifiant reproduit les mêmes surfaces. Les surfaces sont fermées autour du joint, avec faces et normales locales. Leur géométrie est visible dans la vue principale de la pièce et les vues 3D opérateur. Les profils et maillages sont inclus dans la scène RV exportée.

Les références d’échos géométriques utilisent ces profils. Une pondération heuristique dépend de l’incidence sur les facettes. Aucun bruit temporel ou pic indépendant de la géométrie n’est ajouté. Cela reste un modèle pédagogique de rétrodiffusion : les coefficients physiques et le tracé complet des réflexions sur ces maillages ne sont pas résolus. Les interfaces principales du tracé restent cylindriques. Le champ scalaire direct reste un calcul en milieu homogène masqué au domaine principal.

## Structures cristallographiques

Le panneau **Microstructure — description pour étape suivante** permet de consigner : grains équiaxes, colonnaires ou mixtes ; taille nominale ; orientation préférentielle. La description est conservée dans les exports matière et scène RV.

À ce stade ce sont des métadonnées uniquement. Aucun rendu de grains, aucune propagation anisotrope, atténuation par la taille des grains ou diffusion cristallographique n’est revendiqué. Pour coupler ces effets, il faudra définir les zones (métal de base, ZAT, métal fondu), leurs orientations, lois élastiques et paramètres de diffusion, puis vérifier le modèle physique correspondant.

Les graphiques et signaux actuels ne doivent pas être présentés comme une simulation CIVA élastodynamique validée.
