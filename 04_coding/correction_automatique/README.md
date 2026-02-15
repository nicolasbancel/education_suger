# Correction automatique d'exercices – Physique-Chimie

Un outil Python complet qui permet de générer automatiquement des **fiches LaTeX de correction d'exercices**, à partir :
- d'**images d'énoncés scannés**,
- de **fichiers `.tex` existants**,
- ou bientôt de **PDF d'annales**.

Ce projet est pensé à la fois pour :
- 🧑‍🏫 **les enseignants**, qui souhaitent générer rapidement des corrections bien formatées ;
- 🧑‍💻 **les développeurs**, qui souhaitent adapter le pipeline à d'autres matières ou formats.

---

## ✨ Fonctionnalités principales

- 🔍 Extraction intelligente de l'énoncé et des questions depuis des fichiers LaTeX.
- 🪄 Génération automatique des corrections en langage LaTeX via **GPT-4o (OpenAI)**.
- 🧩 Insertion des solutions directement dans le document, avec des marqueurs de type `%CORRECTION:Q1E2%`.
- 🖼️ Gestion dynamique des images associées aux énoncés.
- 📦 Organisation modulaire pour intégration facile dans d'autres projets.

---

## 🚀 Installation

### 1. Prérequis

- Python 3.10+
- [Poetry](https://python-poetry.org/) pour la gestion des dépendances
- Un compte OpenAI avec clé API

### 2. Clonage et configuration

```bash
git clone https://github.com/nicolasbancel/education_suger.git
cd education_suger/09_coding
poetry install
cp .env.example .env  # créez un fichier .env avec votre clé API
```
Ajoutez dans .env :
`OPENAI_API_KEY=sk-...`


## 🧪 Exemples d'utilisation

### À partir d’un fichier `.tex` structuré

Ce mode permet d’extraire automatiquement les exercices et questions depuis un fichier `.tex`, d’y insérer des marqueurs de correction, de générer les solutions via GPT-4o, puis de les intégrer au bon endroit dans le fichier LaTeX.

```bash
poetry run python main.py from_latex /Users/nicolasbancel/git/education_suger/02_3ème_CI_pc/ds/brevet_blanc_2.tex

poetry run python main.py from_latex /Users/nicolasbancel/git/education_suger/01_1ères_STD2A_pc/ds/bac_blanc_1ereSTD2A_PC_no2.tex

poetry run python /utils/meta/correction_framework.py
```

### À partir d’un dossier d’images

Ce mode scanne toutes les images `.jpg`, `.png`, etc., présentes dans le dossier, génère une solution LaTeX pour chacune via OpenAI, et les assemble dans une fiche LaTeX.

### Commands

```bash

cd /Users/nicolasbancel/git/education_suger/09_coding/src

poetry run python main.py from_image /Users/nicolasbancel/git/education_suger/01_1ères_STD2A_pc/chap5_lumiere/a_corriger


```

### Other paths

```
/Users/nicolasbancel/git/education_suger/00_1ères_STD2A_maths/08_probabilités/fiche_1
```


