## Correctif ergonomique — vue du piquage restaurée en premier

Quatre onglets : 1 Piquage 3D, 2 Réglages de la pièce, 3 Scan manuel, 4 Mode d’emploi. Le planificateur et les exemples avancés restent dans les réglages ; ils ne remplacent pas la vue du piquage. Une seule sélection MWB commande le scan. Sous Windows, double-cliquer **LANCER_NOZZLE.bat**. Lire **GUIDE_OPERATEUR_FR.md** pour le parcours détaillé.

# BYTE NDT — NOZZLE GEOMETRY TWIN REV0.4

Version de travail pour formation et préparation d’examen. Le scan manuel est désormais raccordé à la géométrie nozzle et aux cinq indications de la configuration. Le panneau historique de tôle reste disponible en référence repliée.

## Démarrage

Python 3.12 recommandé. Depuis ce dossier :

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python -m streamlit run app.py
```

Sous Windows :

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements-lock.txt
.venv\Scripts\python -m streamlit run app.py
```

Dans l’environnement cloud préparé :

```sh
cd /workspace/01_Paut_Training_-
/workspace/nozzle-venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501 --browser.gatherUsageStats false
```

Le déploiement public https://byte-ndt-twin-formation-rev1.streamlit.app/ n’est pas modifié par cette archive.

## Mode d’emploi — première pièce test

1. Choisir FR/EN et TRAINING ou REAL_EXAM_PREPARATION. Régler les diamètres, épaisseurs, angle, décalage et longueurs dans la barre latérale. Les contrôles refusent les dimensions incompatibles avec l’enveloppe retenue.
2. Régler la préparation radiale approchée : angle, jeu, talon, renfort. Ces surfaces ne constituent pas un solide CAO validé.
3. Choisir la MWB monoélément : 45°, 60° ou 70°, chacune en 2, 4 ou 5 MHz. La configuration MWB de la section accès/scan est celle utilisée par l’écran opérateur. Les encombrements réels du sabot sont à renseigner ; le symbole de sonde n’est pas son volume.
4. Dans les zones de scan, fixer les limites angulaires et Z, les dimensions disponibles, le sabot, la course et les marges. TO_ASSESS lance la comparaison d’encombrement ; INACCESSIBLE exclut une zone, dont il faut préciser la cause. Une exclusion sans limites bloque tout le scan. UNASSESSED signifie non évalué, jamais accès validé.
5. Régler la plage et le pas de scan. Le plan est en créneaux/méandre. Le CSV et le JSON conservent les exclusions et les statuts. Le plan ne certifie pas la couverture volumique.
6. Nommer la pièce et ajuster les cinq indications : deux collages/manques de fusion 6 × 3 mm sur flancs, inclusion diamètre 2 mm, deux fissures de choc thermique 4 × 2 mm. Ces valeurs sont des paramètres modifiables. Fixer azimut, Z, profondeur radiale depuis l’extérieur et orientation locale depuis +Z. Les coordonnées manquantes restent null dans l’export ; les indications non positionnées ne génèrent aucun signal. Le positionnement automatique conforme aux flancs réels n’est pas calculé. La largeur n’est pas assimilée à une hauteur radiale.
7. Dans **Scan manuel du nozzle**, saisir la sonde à la souris et glisser en créneaux. La trace bleue montre le geste. Créneaux ▶ démontre le parcours ; Pause rend la main. Les points bloqués et l’ouverture ne produisent pas de rayon. En zone non évaluée, l’exploration géométrique reste visible avec son statut, sans valider l’accès.
8. Sur une réponse pédagogique, arrêter le déplacement et tourner légèrement : molette au voisinage du palpeur, ou boutons ±1°. Comparer le maximum affiché dans la porte choisie. Les valeurs restent heuristiques et non étalonnées.
9. Choisir A, B ou C, régler les bornes temporelles et le seuil relatif. Enregistrer plusieurs points autour du maximum pour l’étendue indicative à −6 dB. Il s’agit de l’étendue des points échantillonnés, pas d’une dimension de défaut certifiée.
10. Vue coupe : les rayons sont calculés en 3D dans la paroi cylindrique principale, puis projetés en Z/profondeur radiale. Vue **Nozzle 3D + rayons** : glisser dans cette vue pour tourner la caméra, molette pour zoomer, Vue initiale pour réinitialiser. Ce geste est distinct du déplacement du palpeur sur la vue déroulée.
11. Mode instructeur : révéler les cinq indications positionnées. Exporter les paramètres via Streamlit et le scan manuel via le bouton **Exporter** du panneau opérateur. Les points manuels restent dans le composant navigateur : exporter avant de modifier une configuration Streamlit ou de recharger la page.

## Ce qui fonctionne et ce qui reste à raccorder

- Géométrie nozzle paramétrique, courbes XYZ, matériaux, lexique FR/EN et exports CSV conservés de REV0.3.
- Scan manuel raccordé aux paramètres courants, déplacement avec capture du pointeur et conservation du point de saisie, rafraîchissement regroupé par image navigateur ; caméra distincte du palpeur.
- Réflexions géométriques spéculaires sur les cylindres intérieur/extérieur du tube principal, arrêt aux extrémités et à l’enveloppe d’ouverture. Faisceau : éventail illustratif ±5°, pas un champ d’amplitude calculé. Propagation complète dans la branche, la préparation et le volume soudé non résolue.
- En TRAINING, réponses des indications positionnées calculées par une heuristique géométrique non étalonnée ; aucune diffraction ou réponse matériau validée. En REAL_EXAM_PREPARATION, aucun signal synthétique présenté comme acquisition réelle : aucune acquisition n’est connectée.
- Cascade et CAD/TCG : emplacements de modules non raccordés. Référence US 319/P15 et révision à vérifier avant intégration des critères. Kirchhoff, Born, GTD : choix futurs, moteurs non implémentés.
- Aucune validation de conformité industrielle ou de couverture complète. Les exemples 3D exploratoires de la vue Plotly restent indépendants du registre projet ; l’écran manuel utilise bien le registre des cinq indications.

## Vérification

```sh
/workspace/nozzle-venv/bin/python -m unittest test_geometry test_scan -v
```

Huit tests géométrie/scan. Exécution FR/EN via Streamlit AppTest. Tests Chromium optionnels avec Python système et Playwright : `python test_operator_browser.py` (Chromium installé attendu dans `/usr/bin/chromium`). Vérifient rayons cylindriques, glissement, absence de saut à la saisie, capture/relâchement hors canvas, rotation, créneaux/pause, export, exclusions et absence de signal synthétique en mode examen. La fluidité observée sur cette machine n’est pas une garantie sur tout poste.

Sources historiques : dépôt `jmpuybouffat/BYTE-NDT-TWIN-FORMATION-ALPHA`, écran original conservé dans `operator_view_legacy.html` ; archive utilisateur REV0.3 pour le nozzle. Aucun envoi à des tiers ni publication sur le site public.

## English quick guide

Set pipe/joint/material parameters, select the single-element MWB in the scan-access section, define accessible/excluded scan zones, and position the five project indications. Drag the probe on the unwrapped main pipe in a raster, then rotate slightly with the wheel or ±1° controls to seek the displayed training maximum. Use A/B/C gates and record samples. Switch the ray view to 3D; camera drag/zoom is independent from probe manipulation. Export manual scan data before reloading or changing the Streamlit configuration. Geometric rays and training echoes are illustrative; DAC/TCG, cascade, Born/Kirchhoff/GTD and real acquisition are not implemented.
