import os

gitignore_code = """.env
venv/
.venv/
__pycache__/
*.pyc
data/*.csv
data/rapports/*.pdf
models/
.DS_Store
Thumbs.db
.vscode/
*.log
"""

dockerfile_code = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""

docker_compose_code = """version: '3.8'
services:
  audit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - .:/app
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
"""

readme_code = """# Audit FDS + LLM — Conformite Reglementaire

Audit automatique de conformite des produits de nettoyage industriel
aux normes REACH, CLP et Ecolabel EU, avec analyse par intelligence artificielle.

---

## Pourquoi ce projet ?

Les entreprises de nettoyage industriel utilisent des dizaines de produits chimiques.
Verifier manuellement la conformite de chaque produit aux normes europeennes
(REACH, CLP, directive COV, Ecolabel EU) est une tache longue, technique et a risque.

Ce projet automatise entierement cet audit : il analyse les indicateurs de chaque
produit, detecte les ecarts reglementaires, et genere un rapport detaille
avec recommandations — en quelques secondes.

---

## Ce que le systeme analyse

Pour chaque produit, le pipeline verifie :
- COV (Composes Organiques Volatils) vs directive 1999/13/CE (seuil : 30 g/L)
- Biodegradabilite vs criteres Ecolabel EU (seuil : 60%)
- Ecotoxicite aquatique LC50 vs classification CLP (seuil : 10 mg/L)
- Conformite REACH et enregistrement ECHA
- pH dans les limites de securite (4 a 11)

Un score de conformite sur 100 est calcule pour chaque produit,
avec trois niveaux : Conforme, Modere, Critique.

---

## Architecture

    src/pipelines/
        extract.py       Extraction des donnees FDS (simulation ou vrais PDF)
        transform.py     Calcul des scores et alertes reglementaires
        run_pipeline.py  Orchestration ETL

    src/llm/
        analyzer.py      Analyse par LLM (OpenAI GPT-4o-mini ou simulation)
        reporter.py      Generation du rapport PDF (ReportLab)

    dashboard/
        app.py           Dashboard Streamlit interactif

    data/
        fds_raw.csv      Donnees brutes extraites
        fds_clean.csv    Donnees enrichies avec scores
        rapports/        Rapports PDF generes

---

## Lancement rapide

    pip install -r requirements.txt
    python run.py
    streamlit run dashboard/app.py

## Avec Docker

    docker compose up --build

## Configuration OpenAI (optionnel)

Creer un fichier .env a la racine :

    OPENAI_API_KEY=sk-...votre_cle...

Sans cle API, le systeme fonctionne en mode simulation avec des analyses pre-definies.

---

## Resultats

    Produits analyses : 5
    Conformes         : 3 (60%)
    Critiques         : 2 (40%)

    Produits critiques identifies :
    - Degraissant solvant chlore HD  (10/100) — COV x3.9, non-conforme REACH
    - Decapant sol industriel        (10/100) — COV x4.8, 3 substances SVHC

---

## Auteur

Data Engineer passionne par l industrie et la conformite reglementaire.
Profil hybride : competences techniques (Python, LLM, pipelines de donnees)
et experience terrain dans le secteur du nettoyage industriel.

GitHub : https://github.com/TON_USERNAME
"""

open('.gitignore',        'w', encoding='utf-8').write(gitignore_code)
open('Dockerfile',        'w', encoding='utf-8').write(dockerfile_code)
open('docker-compose.yml','w', encoding='utf-8').write(docker_compose_code)
open('README.md',         'w', encoding='utf-8').write(readme_code)
print('Tous les fichiers OK')