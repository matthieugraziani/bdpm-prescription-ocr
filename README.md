# 💊 BDPM Prescription OCR

[![CI](https://github.com/matthieugraziani/bdpm-prescription-ocr/actions/workflows/ci.yml/badge.svg)](https://github.com/matthieugraziani/bdpm-prescription-ocr/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)

Application **Streamlit** qui extrait automatiquement les médicaments mentionnés sur une ordonnance (image ou PDF) grâce à l'OCR, corrige les erreurs de reconnaissance par fuzzy matching, puis interroge l'**API BDPM** (Base de Données Publique des Médicaments) pour afficher les informations officielles correspondantes.

## Sommaire

- [Fonctionnement](#fonctionnement)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Tests](#tests)
- [Limites connues & pistes d'amélioration](#limites-connues--pistes-damélioration)

## Fonctionnement

1. L'utilisateur importe une image (PNG/JPG) ou un PDF d'ordonnance, ou colle directement le texte.
2. Pour un PDF, chaque page est convertie en image via **PyMuPDF**.
3. Chaque image passe par un prétraitement **OpenCV** (niveaux de gris, débruitage, seuillage adaptatif) pour améliorer la lisibilité avant OCR.
4. Le texte est extrait ligne par ligne avec **EasyOCR** (modèle français).
5. Chaque ligne est comparée par fuzzy matching (**RapidFuzz**, scorer `WRatio`) à une liste de noms de médicaments connus, afin de corriger les imperfections de l'OCR.
6. Si le score de similarité dépasse le seuil de confiance (réglable dans l'interface), le nom retenu est envoyé à l'**API BDPM** pour récupérer les informations officielles du médicament.
7. Les résultats sont affichés ligne par ligne, regroupés dans un tableau récapitulatif, et exportables en CSV.

## Fonctionnalités

- Import d'image (PNG/JPG) ou de PDF multi-pages
- Saisie manuelle de texte en alternative à l'OCR
- Prétraitement d'image pour fiabiliser la reconnaissance (OpenCV)
- OCR en français via EasyOCR
- Correction des erreurs OCR par fuzzy matching (RapidFuzz)
- Seuil de confiance de matching réglable depuis l'interface (50–100 %)
- Interrogation de l'API BDPM pour chaque médicament reconnu, avec gestion des erreurs réseau/HTTP
- Indicateur de statut de l'API BDPM (en ligne / hors ligne) dans la barre latérale
- Affichage détaillé par ligne d'ordonnance + tableau récapitulatif
- Export des résultats au format CSV

## Architecture

```
.
├── app.py                   # Point d'entrée Streamlit (UI + orchestration)
├── config.py                 # Configuration (URL de l'API BDPM)
├── api/
│   └── bdpm_client.py         # Client HTTP vers l'API BDPM (recherche + statut)
├── ocr/
│   └── extractor.py           # Prétraitement image (OpenCV) + extraction OCR (EasyOCR)
├── matcher/
│   └── fuzzy_match.py          # Normalisation et fuzzy matching des noms de médicaments
├── services/
│   └── analyzer.py             # Orchestration : lignes OCR → matching → API → résultats
├── ui/
│   └── components.py           # Composants d'affichage Streamlit (statut API, résultats)
└── tests/                      # Tests unitaires (pytest)
```

## Installation

Prérequis : Python 3.11+

```bash
git clone https://github.com/matthieugraziani/bdpm-prescription-ocr.git
cd bdpm-prescription-ocr

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

> EasyOCR télécharge les modèles de reconnaissance au premier lancement ; la première analyse peut donc prendre plus de temps.

## Configuration

L'URL de l'API BDPM est lue depuis la variable d'environnement `BDPM_API_URL`. Copier le fichier d'exemple :

```bash
cp .env.example .env
```

Valeur par défaut (API BDPM hébergée sur Render) :

```
BDPM_API_URL=https://bdpm-database.onrender.com
```

## Utilisation

```bash
streamlit run app.py
```

1. Importer une image ou un PDF d'ordonnance, ou coller le texte directement.
2. Ajuster si besoin le seuil de confiance du fuzzy matching.
3. Cliquer sur **Analyser**.
4. Consulter le détail par ligne et télécharger le tableau récapitulatif en CSV.

## Tests

```bash
pytest
```

La suite couvre le fuzzy matching, le client API BDPM (succès, erreurs réseau/HTTP, JSON invalide) et l'orchestration de l'analyse. Elle est exécutée automatiquement par la CI GitHub Actions à chaque push et pull request.

## Limites connues & pistes d'amélioration

- La liste de référence utilisée pour le fuzzy matching (`matcher/fuzzy_match.py`) ne couvre qu'une vingtaine de médicaments courants ; elle devrait être remplacée par les dénominations réelles exposées par l'API BDPM.
- Les résultats de l'API BDPM sont actuellement affichés en JSON brut plutôt que d'être parsés en colonnes dédiées (dénomination, dosage, code CIS, etc.).
- L'OCR s'exécute en CPU par défaut (`gpu=False`) ; l'activation du GPU peut accélérer le traitement sur les machines compatibles.

## Stack technique

Streamlit · EasyOCR · OpenCV · RapidFuzz · PyMuPDF · Pandas · Requests
