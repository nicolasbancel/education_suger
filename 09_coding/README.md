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
