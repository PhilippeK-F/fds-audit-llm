import pandas as pd
import numpy as np

SEUILS = {
    "cov_max_g_par_l":          30.0,
    "biodegradabilite_min_pct": 60.0,
    "lc50_min_mg_l":            10.0,
    "ph_min":                    4.0,
    "ph_max":                   11.0,
}

def transform(df):
    df = df.copy()
    df.columns = [c.lower().strip() for c in df.columns]
    df = df.drop_duplicates()
    df["alerte_reach"] = ~df["conforme_reach"]
    df["alerte_cov"] = df["cov_g_par_l"] > SEUILS["cov_max_g_par_l"]
    df["ecart_cov"] = (df["cov_g_par_l"] - SEUILS["cov_max_g_par_l"]).round(2).clip(lower=0)
    df["alerte_biodeg"] = df["biodegradabilite_pct"] < SEUILS["biodegradabilite_min_pct"]
    df["ecart_biodeg"] = (SEUILS["biodegradabilite_min_pct"] - df["biodegradabilite_pct"]).round(2).clip(lower=0)
    df["alerte_lc50"] = df["lc50_mg_l"] < SEUILS["lc50_min_mg_l"]
    df["alerte_ph"] = ~df["ph"].between(SEUILS["ph_min"], SEUILS["ph_max"])
    df["score_conformite"] = 100
    df.loc[df["alerte_reach"],  "score_conformite"] -= 30
    df.loc[df["alerte_cov"],    "score_conformite"] -= 25
    df.loc[df["alerte_biodeg"], "score_conformite"] -= 20
    df.loc[df["alerte_lc50"],   "score_conformite"] -= 15
    df.loc[df["alerte_ph"],     "score_conformite"] -= 10
    df["score_conformite"] = df["score_conformite"].clip(lower=0)
    df["niveau_risque"] = pd.cut(
        df["score_conformite"],
        bins=[0, 40, 70, 100],
        labels=["Critique", "Modere", "Conforme"]
    ).astype(str)
    cols_alertes = ["alerte_reach", "alerte_cov", "alerte_biodeg", "alerte_lc50", "alerte_ph"]
    df["nb_alertes"] = df[cols_alertes].sum(axis=1)
    print("[transform] " + str(len(df)) + " produits analyses")
    print("[transform] Produits non conformes : " + str((df["score_conformite"] < 70).sum()))
    return df

if __name__ == "__main__":
    df_raw = pd.read_csv("data/fds_raw.csv")
    df_clean = transform(df_raw)
    print(df_clean[["produit", "score_conformite", "niveau_risque", "nb_alertes"]])