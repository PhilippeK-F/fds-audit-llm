## Pourquoi ce projet ?

Les entreprises de nettoyage industriel utilisent des dizaines de produits chimiques.
Vérifier manuellement la conformité de chaque produit aux normes européennes
(REACH, CLP, directive COV, Écolabel EU) est une tâche longue, technique et à risque.

Ce projet automatise entièrement cet audit : il analyse les indicateurs de chaque
produit, détecte les écarts réglementaires, et génère un rapport détaillé
avec recommandations — en quelques secondes.

---

## FDS = Fiche de Données de SécuritéFDS = Fiche de Données de Sécurité

C'est le document obligatoire fourni par chaque fabricant de produit chimique. Il contient :

La composition du produit
Les dangers pour la santé et l'environnement
Les équipements de protection nécessaires
La conformité REACH, CLP...

---

## Ce que le système analyse

Pour chaque produit, le pipeline vérifie :
- COV (Composés Organiques Volatils) vs directive 1999/13/CE (seuil : 30 g/L)
- Biodégradabilité vs critères Écolabel EU (seuil : 60%)
- Écotoxicité aquatique LC50 vs classification CLP (seuil : 10 mg/L)
- Conformité REACH et enregistrement ECHA
- pH dans les limites de sécurité (4 à 11)

Un score de conformité sur 100 est calculé pour chaque produit,
avec trois niveaux : Conforme, Modéré, Critique.

---

## Architecture

    src/pipelines/
        extract.py       Extraction des données FDS (simulation ou vrais PDF)
        transform.py     Calcul des scores et alertes réglementaires
        run_pipeline.py  Orchestration ETL

    src/llm/
        analyzer.py      Analyse par LLM (OpenAI GPT-4o-mini ou simulation)
        reporter.py      Génération du rapport PDF (ReportLab)

    dashboard/
        app.py           Dashboard Streamlit interactif

    data/
        fds_raw.csv      Données brutes extraites
        fds_clean.csv    Données enrichies avec scores
        rapports/        Rapports PDF générés

---

## Lancement rapide

    pip install -r requirements.txt
    python run.py
    streamlit run dashboard/app.py

## Avec Docker

    docker compose up --build

## Configuration OpenAI (optionnel)

Créer un fichier .env à la racine :

    OPENAI_API_KEY=sk-...votre_cle...

Sans clé API, le système fonctionne en mode simulation avec des analyses pré-définies.

---

## Résultats

    Produits analysés : 5
    Conformes         : 3 (60%)
    Critiques         : 2 (40%)

    Produits critiques identifiés :
    - Dégraissant solvant chloré  (10/100) — COV x3.9, non-conforme REACH
    - Décapant sol industriel     (10/100) — COV x4.8, 3 substances SVHC

---

## Auteur

Philippe Kirstetter-Fender 

Data Engineer passionné par l'industrie et la conformité réglementaire.
Profil hybride : compétences techniques (Python, LLM, pipelines de données)
et expérience terrain dans le secteur du nettoyage industriel.
