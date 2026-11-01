# Vérification des traductions FR/EN

Correction des valeurs de type et d’emplacement des indications, des en-têtes de tableaux et des choix de scénario/morphologie. Les boutons, options et messages du panneau opérateur utilisent la langue choisie. Le guide complet est disponible en français et en anglais. Le panneau historique de tôle s’initialise dans la langue choisie.

Les clés de données, identifiants de pièces et codes internes restent stables pour les calculs et les exports. Les textes libres saisis par l’utilisateur ne sont pas réécrits automatiquement.

Les paramètres de widgets possèdent des clés persistantes. Les tableaux conservent un état canonique distinct de leur texte d’affichage : le changement FR/EN préserve les dimensions, les poses et les zones exclues, y compris les lignes ajoutées, sans duplication. Les tests couvrent aussi FR → EN → FR.

Les descriptions de portée ont été mises à jour : le scan possède un contrôle géométrique approché et des cartes de champ ; cela ne signifie pas collision CAO complète, couverture totale ou calcul élastodynamique validé.
