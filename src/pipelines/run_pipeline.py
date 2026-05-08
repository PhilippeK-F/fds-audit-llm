import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.pipelines.extract import extract
from src.pipelines.transform import transform

def load(df, output_path="data/fds_clean.csv"):
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)
    print("[load] Fichier sauvegarde -> " + output_path)

def main():
    print("=" * 50)
    print("PIPELINE AUDIT FDS - DEMARRE")
    print("=" * 50)

    print("\n1. Extraction des FDS...")
    df_raw, fds_simulees = extract(output_path="data/fds_raw.csv")

    print("\n2. Analyse de conformite...")
    df_clean = transform(df_raw)

    print("\n3. Sauvegarde...")
    load(df_clean, output_path="data/fds_clean.csv")

    print("\n" + "=" * 50)
    print("PIPELINE TERMINE")
    print("  Produits analyses  : " + str(len(df_clean)))
    print("  Produits conformes : " + str((df_clean["score_conformite"] >= 70).sum()))
    print("  Produits critiques : " + str((df_clean["score_conformite"] < 40).sum()))
    print("  Fichier            : data/fds_clean.csv")
    print("=" * 50)
    return df_clean, fds_simulees

if __name__ == "__main__":
    main()
