# Adresse publique communiquée par Jean-Michel

https://byte-ndt-nozzle-formation.streamlit.app/

Déploiement confirmé par Jean-Michel. Aucun mail envoyé par l’assistant.

# Publication Streamlit — priorité Marlier et Fabien

Le code de la version RÉTRO SCALAIRE et les protocoles FR/EN sont publiés sur GitHub. Une publication GitHub ne crée pas automatiquement une application Streamlit publique.

## Création dans le compte Streamlit Community Cloud

1. Ouvrir https://share.streamlit.io/ et se connecter au compte qui a accès au dépôt GitHub.
2. Cliquer **Create app**, puis choisir le déploiement depuis GitHub (formulation susceptible de varier selon l’interface).
3. Saisir :

| Champ | Valeur |
|---|---|
| Repository | jmpuybouffat/01_Paut_Training_- |
| Branch | main |
| Main file path | app.py |
| Python (Advanced settings) | 3.12 |

4. Aucun secret applicatif n’est requis. Choisir un sous-domaine disponible si le formulaire le propose, puis cliquer **Deploy**.
5. Attendre le démarrage et copier l’adresse publique réellement fournie par Streamlit. Ne pas envoyer l’adresse localhost du PC.

Cette création demande une session Streamlit/GitHub dans le navigateur de Jean-Michel. La session du compte n’est pas accessible depuis l’environnement de travail de l’assistant. Aucun lien public de cette nouvelle application n’est annoncé comme créé sans confirmation du service.

## Contrôle avant partage

- Vérifier la mention de version RÉTRO SCALAIRE.
- Ouvrir 3 · Scan manuel et charger le test témoin rétrodiffusion — MWB 45° / 4 MHz. Cela remplace les réglages personnels.
- Attendre le calcul ; vérifier surface finie, champ coloré, écho de centre voisin de 8,73 µs et commande Zoom indication calculée.
- Passer en EN et ouvrir le protocole : son contenu complet doit être anglais.
- Pour Fabien : Exporter scène RV ; vérifier les données scalar_scattering.field_samples_world et les poses. Ce sont des données pour un client RV, pas une interface immersive terminée.
- Ouvrir le lien depuis un autre navigateur/une fenêtre privée pour contrôler son accessibilité.
- Remplacer le marqueur [LIEN STREAMLIT À INSÉRER APRÈS PUBLICATION] dans les deux mails prioritaires. Aucun envoi automatique n’est réalisé.

## Limites à transmettre

Premier modèle scalaire monochromatique, incidence directe et diffusion unique sur surface finie, réception intégrée sur ouverture MWB. Pas de rebonds du champ diffusé sur les parois ni de solveur élastique complet. Les moteurs internes C1/C2 ne sont pas encore raccordés à cette application. Version PA et compatibilité de réglages instrument à venir. L’application ne réalise pas d’acquisition réelle.
