import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.pipelines.extract import extract
from src.pipelines.transform import transform
from src.llm.analyzer import analyser_tous
from src.llm.reporter import generer_rapport

def main():
    print("=" * 50)
    print("AUDIT FDS + LLM - DEMARRE")
    print("=" * 50)

    print("\n1. Extraction des FDS...")
    df_raw, fds_simulees = extract(output_path="data/fds_raw.csv")

    print("\n2. Analyse de conformite...")
    df_clean = transform(df_raw)

    df_clean.to_csv("data/fds_clean.csv", index=False)

    print("\n3. Analyse LLM par ChatGPT...")
    resultats = analyser_tous(df_clean, fds_simulees)

    print("\n4. Generation du rapport PDF...")
    for r in resultats:
        fds = next((f for f in fds_simulees if f["produit"] == r["produit"]), {})
        r["fournisseur"] = fds.get("fournisseur", "-")
    generer_rapport(resultats, output_path="data/rapports/audit_fds.pdf")

    print("\n" + "=" * 50)
    print("AUDIT TERMINE")
    print("  Produits analyses  : " + str(len(resultats)))
    print("  Conformes          : " + str(sum(1 for r in resultats if r["score_conformite"] >= 70)))
    print("  Critiques          : " + str(sum(1 for r in resultats if r["score_conformite"] < 40)))
    print("  Rapport PDF        : data/rapports/audit_fds.pdf")
    print("=" * 50)

if __name__ == "__main__":
    main()
