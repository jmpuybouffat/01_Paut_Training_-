# Mise en ligne Streamlit Community Cloud

Le dépôt contient une application Streamlit et un scénario pédagogique prêt à balayer. Une publication GitHub ne crée pas automatiquement une application Streamlit publique.

Dans votre compte Streamlit Community Cloud, créer une application avec :

- Repository : `jmpuybouffat/01_Paut_Training_-`
- Branch : `main`
- Main file path : `app.py`
- Version Python recommandée : 3.12

Aucun secret applicatif n’est requis pour ce démonstrateur. Le dossier `.streamlit` contient les réglages d’affichage et de télémétrie. Le fichier `requirements.txt` contient les dépendances directes ; `requirements-lock.txt` conserve les versions testées localement. Le service choisit normalement requirements.txt pour le déploiement.

Après publication, vérifier les quatre onglets et ouvrir **3 · Scan manuel**. Avec TRAINING / DEMO_GESTE_PAROI (MWB 45° / 4 MHz par défaut, 5 MHz sélectionnable) : les cinq cibles artificielles sont définies dans la paroi principale, le mode instructeur est décoché, l’A-scan fonctionne pour le scénario, et le faisceau pédagogique est activé. Cette démo n’est pas le placement physique de défauts sur les flancs de soudure.

Essai fonctionnel : lancer Créneaux, mettre en Pause, déplacer la sonde sur la surface 3D, tourner par ±1°, vérifier le changement de réponse et les vues synchronisées, inverser le parcours et exporter un point. Vérifier que la vue élève ne révèle pas les positions et que le mode préparation examen ne génère pas de signal présenté comme une acquisition réelle.

Le déploiement requiert votre session Streamlit/GitHub dans votre navigateur. Le dépôt préparé ne prouve pas que la publication est faite ; aucun lien public de cette nouvelle application n’est revendiqué sans confirmation du service.
