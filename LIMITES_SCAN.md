# Scan borné et arrêts opérateur

Le déplacement manuel (surface 3D et déroulé) et le raster automatique partagent les mêmes contrôles. Le point d’entrée reste dans les limites angulaires et Z du plan. Une enveloppe rectangulaire centrée de sabot 24 × 14 mm, augmentée de la marge définie dans les réglages, est contrôlée contre les extrémités du tube, les zones exclues et l’emprise approchée du piquage/préparation.

C’est une approximation géométrique de formation : décalage réel du point d’émergence dans le sabot, contact courbe et collision complète du volume CAO ne sont pas validés. L’absence de collision ne constitue pas une démonstration de couverture UT.

Les déplacements sont vérifiés par sous-pas, pour ne pas sauter une zone interdite avec un grand mouvement. Les zones explicitement exclues sont comparées à l’enveloppe orientée du sabot par recouvrement de polygones ; les bandes exclues fines ne sont pas simplement ignorées entre deux points. Une zone exclue sans limites utilisables bloque le déplacement. Une zone non évaluée reste identifiée comme telle et autorise seulement une exploration géométrique de formation.

À un obstacle, le point de sonde reste à sa dernière position admise, le mouvement s’arrête et un motif apparaît. Le raster s’arrête à la fin du plan et ne recommence pas tout seul. Inverser le parcours permet de revenir, y compris après un arrêt au milieu d’un segment. Réinitialiser recommence le scénario.

**STOP / Pause** arrête le mouvement. Après avoir activé la vue opérateur, **Espace** ou **Échap** arrête également le déplacement ; Échap fonctionne même pendant l’édition d’un contrôle du panneau. La capture de souris est relâchée à un arrêt géométrique. Une rotation de la sonde est aussi refusée si elle ferait entrer l’enveloppe dans une zone interdite.

Les exports contiennent les événements `motion_stop_events` / `motion_limits.stop_events`, avec la pose, le motif et le temps écoulé du document navigateur. L’événement JavaScript local `BYTE_NDT_MOTION_STOP` permet une intégration RV. Aucun ordre matériel ni envoi réseau n’est généré.

Les échelles de la coupe et du champ pédagogique sont fixes relativement au palpeur pour un angle et une épaisseur donnés : une troncature de trajet ne provoque plus un zoom automatique donnant l’impression d’un faisceau qui change. La sonde reste monoélément ; le raster ne modifie pas son angle de réfraction.

Le sélecteur Born/Kirchhoff/GTD est désactivé et identifié comme futur : il ne produisait aucune comparaison physique. La réponse physique et la visualisation des interactions depuis les indications sont reportées à l’étape suivante, conformément à la priorité donnée par l’utilisateur au bornage du scan. L’A-scan pédagogique existant est actif en TRAINING ; REAL_EXAM_PREPARATION ne possède aucune acquisition réelle connectée.

Vérifications : extrémités, piquage, bande exclue fine, geste manuel dans le déroulé, arrêt du raster sans traverser l’obstacle, retour après arrêt partiel, arrêt clavier et échelle stable. Script : `python test_scan_limits_browser.py` avec Playwright et Chromium système.
