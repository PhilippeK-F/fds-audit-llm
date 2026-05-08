# Audit FDS + LLM — Conformité Réglementaire

Audit automatique de conformité des produits de nettoyage industriel
aux normes REACH, CLP et Ecolabel EU, avec analyse par intelligence artificielle.

---

## Pourquoi ce projet ?

Les entreprises de nettoyage industriel utilisent des dizaines de produits chimiques.
Vérifier manuellement la conformité de chaque produit aux normes européennes
(REACH, CLP, directive COV, Ecolabel EU) est une tâche longue, technique et a risque.

Ce projet automatise entièrement cet audit : il analyse les indicateurs de chaque
produit, détecte les écarts réglementaires, et génère un rapport detaillé
avec recommandations — en quelques secondes.

---
## FDS = Fiche de Données de Sécurité

C'est un document obligatoire que chaque fabricant de produit chimique doit fournir à ses clients professionnels. Elle contient toutes les informations sur :

La composition du produit (substances actives)
Les dangers pour la santé et l'environnement
Les équipements de protection nécessaires
Les premiers secours en cas d'accident
Les conditions de stockage et transport
La conformité réglementaire (REACH, CLP...)

---
## Ce que le système analyse

Pour chaque produit, le pipeline vérifie :
- COV (Composes Organiques Volatils) vs directive 1999/13/CE (seuil : 30 g/L)
- Biodegradabilité vs critères Ecolabel EU (seuil : 60%)
- Ecotoxicite aquatique LC50 vs classification CLP (seuil : 10 mg/L)
- Conformité REACH et enregistrement ECHA
- pH dans les limites de securité (4 a 11)

Un score de conformité sur 100 est calculé pour chaque produit,
avec trois niveaux : Conforme, Modéré, Critique.

---

## Architecture

    src/pipelines/
        extract.py       Extraction des donnees FDS (simulation ou vrais PDF)
        transform.py     Calcul des scores et alertes reglementaires
        run_pipeline.py  Orchestration ETL

    src/llm/
        analyzer.py      Analyse par LLM (OpenAI GPT-4o-mini ou simulation)
        reporter.py      Génération du rapport PDF (ReportLab)

    dashboard/
        app.py           Dashboard Streamlit interactif

    data/
        fds_raw.csv      Données brutes extraites
        fds_clean.csv    Données enrichies avec scores
        rapports/        Rapports PDF generés

---

## Lancement rapide

    pip install -r requirements.txt
    python run.py
    streamlit run dashboard/app.py

## Avec Docker

    docker compose up --build

## Configuration OpenAI (optionnel)

Créer un fichier .env a la racine :

    OPENAI_API_KEY=sk-...votre_clé...

Sans clé API, le systeme fonctionne en mode simulation avec des analyses pre-définies.

---

## Resultats

    Produits analyses : 5
    Conformes         : 3 (60%)
    Critiques         : 2 (40%)

    Produits critiques identifies :
    - Dégraissant solvant chlore HD  (10/100) — COV x3.9, non-conforme REACH
    - Décapant sol industriel        (10/100) — COV x4.8, 3 substances SVHC

---

## Auteur

Philippe Kirstetter-Fender

Data Engineer passionné par l industrie et la conformité réglementaire.
Profil hybride : competences techniques (Python, LLM, pipelines de données)
et experience terrain dans le secteur du nettoyage industriel.


