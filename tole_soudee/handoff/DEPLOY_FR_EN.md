# Déploiement optionnel / Optional deployment

Le HTML autonome fonctionne sans serveur. Pour un accès web Streamlit séparé de Nozzle :

- dépôt / repository: jmpuybouffat/01_Paut_Training_-
- branche / branch: codex/tole-x-cao
- fichier principal / main file: plate_app.py
- dépendances / dependencies: requirements.txt à la racine / at repository root

Ne pas remplacer le service Nozzle existant. Aucun nouveau service Streamlit n’a été créé par cette livraison et aucune URL de service tôle n’est déclarée disponible.

The standalone HTML needs no server. Create a separate Streamlit service if desired; the existing Nozzle service must remain unchanged. No plate deployment URL is supplied or claimed.

Les PDF et manuels HTML sont intégrés au service par plate_app.py. Ils se trouvent dans tole_soudee/manuals. Les boutons PDF ne déclenchent pas de réinitialisation du palpage. Lire STREAMLIT_DEMARRAGE_FR_EN.html pour la fiche pas à pas.

PDF/HTML manuals are included by plate_app.py from tole_soudee/manuals. PDF downloads do not rerun/reset the scanning iframe. Use STREAMLIT_DEMARRAGE_FR_EN.html for the launch checklist.
