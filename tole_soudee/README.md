# BYTE NDT — Tôle soudée / Welded plate P03

🇫🇷 Application pédagogique bilingue : palpage libre et en créneaux, SE à deux cristaux, MWB45/60/70°, PA32 éléments5MHz, vues acoustiques et rapport d’exercice. Les manuels expliquent les vues et proposent des exercices reproductibles. La reprise caméra de Fabien est documentée, sans casque.

🇬🇧 Bilingual teaching prototype: free/raster scanning, dual-crystal SE, MWB45/60/70°,32-element5MHz PA, acoustic views and exercise report. Manuals explain the displays and reproducible exercises. Fabien’s camera-based interface is documented; no headset is assumed.

- [Manuel français — PDF](manuals/MANUEL_FR_P03.pdf)
- [English user manual — PDF](manuals/USER_MANUAL_EN_P03.pdf)
- [Paquet complet P03 avec manuels / Complete package with manuals](https://raw.githubusercontent.com/jmpuybouffat/01_Paut_Training_-/refs/heads/codex/tole-x-cao/downloads/BYTE_NDT_TOLE_P03_AVEC_MANUELS_FR_EN.zip)
- [Dossier Fabien — caméra / Camera handoff](handoff/FABIEN_CAMERA_FR_EN.md)

## Streamlit

Créer une **nouvelle application** depuis son compte Streamlit / Create a **new application** from the owner’s Streamlit account:

| Field | Value |
|---|---|
| Repository | `jmpuybouffat/01_Paut_Training_-` |
| Branch | `codex/tole-x-cao` |
| Main file path | `plate_app.py` |

Python3.12 testé ; dépendances à la racine. Les PDF sont proposés par le service. Aucun service public tôle n’est présumé déjà créé. Nozzle reste une application distincte.

Python3.12 is locally tested; requirements are at repository root. PDF downloads are provided by the service. A public plate service is not presumed to exist. Nozzle remains a separate application.

## Hors ligne / Offline

Extraire tout le ZIP, ouvrir `OUVRIR_APPLICATION.html`, puis lire `MANUEL_FR_P03.pdf` ou `USER_MANUAL_EN_P03.pdf`. Chrome/Edge, aucune installation ni connexion nécessaire.

Extract the entire ZIP and open `OUVRIR_APPLICATION.html`. Read either PDF manual. Chrome/Edge; no installation or Internet required.

## Portée / Scope

Modèle scalaire pédagogique réduit, amplitudes non étalonnées, sabot réel à préciser ; S-scan/cumul par rétroprojection. Pas de qualification industrielle ou d’examen sécurisé. La caméra et sa calibration doivent être raccordées par Fabien. Les captures et contrôles décrits sont des essais logiciels, pas une comparaison expérimentale CIVA/MANTIS/GEKKO.

Reduced scalar teaching model, uncalibrated amplitudes, actual wedge pending; backprojected S-scan/3D responses. No industrial qualification or secure exam platform. Fabien must connect camera tracking/calibration. Captures and checks are software tests, not experimental validation against CIVA/MANTIS/GEKKO.
