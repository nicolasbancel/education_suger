# Architecture MVP – Application d’aide à la préparation des conseils de classe

## 1. Contexte

Je suis enseignant en collège / lycée en France.  
L’établissement utilise **EcoleDirecte** (https://www.ecoledirecte.com/) pour la gestion des notes, appréciations, absences, retards et communications.

La préparation des conseils de classe est extrêmement chronophage pour un professeur principal.

## 2. Problème à résoudre

Pour chaque élève, le professeur principal doit :

1. Rédiger une **appréciation générale trimestrielle**, basée sur :
   - Les appréciations des enseignants de chaque matière  
   - Les notes observées  
   - Les éléments de comportement  

2. Rédiger une **note de synthèse rapide**, incluant :
   - Points forts  
   - Points d’amélioration  
   - Alertes éventuelles (retards, absences, devoirs non rendus, etc.)

3. Proposer une **récompense éventuelle** :
   - Félicitations  
   - Tableau d’honneur  
   - Encouragements  
   - Mention neutre  

Aujourd’hui, cela nécessite :
- Naviguer élève par élève
- Télécharger les bulletins individuellement
- Consolider manuellement les informations

Le processus doit être répété pour plusieurs classes.

## 3. Solution envisagée

Développer une **application web** qui :

1. Se connecte à EcoleDirecte via les identifiants du professeur
2. Récupère la liste des classes
3. Centralise tous les bulletins PDF d’une classe (par trimestre)
4. Convertit les bulletins en texte structuré
5. Génère automatiquement pour chaque élève :
   - Une appréciation générale
   - Une synthèse
   - Une suggestion de récompense

### Évolution prévue

À terme, l’application devra également récupérer :
- Retards récurrents
- Absences
- Mots dans le carnet
- Communications avec les parents
- Nombre de devoirs non rendus

Ces informations peuvent être situées à différents endroits dans EcoleDirecte.

## 4. Rôle attendu de l’IA

Tu es **CTO expert en architecture logicielle, infrastructure cloud et produits tech scalables**.

Tu dois proposer une **architecture technique claire, minimaliste pour le MVP, mais évolutive**, permettant une montée en charge future.

Je coderai la plateforme avec Claude, mais je veux d’abord clarifier l’architecture.

## 5. Objectif de ta réponse

Je veux une réponse structurée et actionnable contenant :

### 1️⃣ Schéma d’architecture (description textuelle)
- Frontend
- Backend
- Workers / traitement asynchrone
- Base de données
- Stockage fichiers
- Pipeline LLM
- Monitoring
- Gestion des secrets

### 2️⃣ Liste des choix technologiques recommandés
Pour chaque choix :
- Technologie recommandée
- Pourquoi
- Alternative possible

### 3️⃣ Pipeline détaillé
Flux complet :
Connexion → récupération → extraction PDF → structuration → génération LLM → restitution

### 4️⃣ Modèle de données minimal
Tables / collections essentielles

### 5️⃣ Plan de déploiement
- Hébergement en France
- MVP rapide
- Évolution vers architecture plus scalable
- Temps envisagé pour coder / développer le MVP de la plateforme
- Contrainte forte : je veux que le MVP soit en local - et je ne veux pas avoir à faire de développement pendant plus d'une semaine.

### 6️⃣ Stratégie d’intégration EcoleDirecte

Contexte :
- Pas d’API officielle publique
- API reverse-engineered par la communauté (pas de garantie que le code soit encore valable)
  - https://github.com/EduWireApps/ecoledirecte-api-docs
  - https://github.com/louislegrain/api-ecoledirecte/

Options possibles :
- Reverse engineering API
- Scraping HTML (possible car le design du site web change très peu)

Tu dois :
- Proposer une stratégie réaliste
- Expliquer les risques (techniques, légaux, maintenance)
- Proposer un plan d’atténuation

## 6. Contraintes & Volume

- 1 professeur = ~4 classes
- 1 classe = ~25 élèves
- Volume moyen par utilisateur : ~100 élèves
- Hébergement : France obligatoire
- Données sensibles (mineurs)

### Sécurité

- Les identifiants EcoleDirecte fournis par les professeurs devront être chiffrés
- Chiffrement en transit (HTTPS)
- Chiffrement au repos
- Isolation des données par utilisateur
- Minimisation des logs contenant des données sensibles

## 7. Fonctionnalités prévues (MVP)

- Authentification de l’enseignant
- Connexion à EcoleDirecte
- Récupération classes & élèves
- Téléchargement des bulletins PDF
- Extraction texte
- Structuration des données :
  - Matière
  - Appréciation
  - Moyenne
  - Absences / retards si présents
- Génération LLM :
  - Appréciation générale
  - Synthèse
  - Suggestion de récompense
- Vue classe centralisée
- Export :
  - CSV
  - DOC
  - PDF

## 8. Contraintes sur l’usage du LLM

Deux modes distincts :

### Mode 1 – Extraction factuelle (CSV)

- Aucune interprétation
- Strictement équivalent au contenu du bulletin
- Pas de reformulation
- Pas d’ajout d’information
- Si donnée absente → champ vide

### Mode 2 – Génération synthétique

- Basée uniquement sur les données extraites
- Pas d’hallucination
- Si incertitude → le signaler
- Interface permettant au professeur :
  - De visualiser le prompt
  - De modifier ton / longueur / vocabulaire

## 9. Exigences non-fonctionnelles

- Architecture minimaliste pour MVP
- Sécurité forte dès le départ
- Coûts maîtrisés
- Scalabilité future (multi-établissements possible)
- Observabilité (logs, erreurs, monitoring)
- Gestion des erreurs robuste (ex : bulletin illisible)

## 10. Format attendu de la réponse

- Sections numérotées correspondant aux points demandés
- Listes claires
- Justifications techniques
- Pas de blabla
- Approche pragmatique orientée MVP → Scalabilité

Si certains éléments nécessitent clarification, explicite les hypothèses que tu prends.
