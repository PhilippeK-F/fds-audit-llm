import os
import pdfplumber
import pandas as pd
from pathlib import Path

# Donnees simulees de FDS pour 5 produits de nettoyage
# En production : remplacer par de vrais PDF fournisseurs
FDS_SIMULEES = [
    {
        "produit": "Degraissant solvant chlore HD",
        "fournisseur": "ChemPro",
        "type_chimique": "solvant",
        "numero_reach": "01-2119457573-36",
        "substances": ["dichloromethane", "tetrachloroethylene"],
        "cov_g_par_l": 118.5,
        "biodegradabilite_pct": 28.0,
        "ph": 7.2,
        "lc50_mg_l": 8.5,
        "ecolabel_eu": False,
        "conforme_reach": False,
        "mention_danger": "H351 - Susceptible de provoquer le cancer",
        "equipements_protection": ["gants nitrile", "lunettes", "masque vapeurs"],
    },
    {
        "produit": "Degraissant biosorce CitraClean",
        "fournisseur": "VerteChimie",
        "type_chimique": "biosorce",
        "numero_reach": "01-2119458244-36",
        "substances": ["d-limonene", "alcool ethylique"],
        "cov_g_par_l": 0.8,
        "biodegradabilite_pct": 94.0,
        "ph": 7.8,
        "lc50_mg_l": 420.0,
        "ecolabel_eu": True,
        "conforme_reach": True,
        "mention_danger": "H226 - Liquide et vapeurs inflammables",
        "equipements_protection": ["gants nitrile"],
    },
    {
        "produit": "Desinfectant quaternaire QAC-50",
        "fournisseur": "ProHygiene",
        "type_chimique": "ammonium quaternaire",
        "numero_reach": "01-2119965703-31",
        "substances": ["chlorure de benzalkonium"],
        "cov_g_par_l": 12.0,
        "biodegradabilite_pct": 45.0,
        "ph": 9.5,
        "lc50_mg_l": 22.0,
        "ecolabel_eu": False,
        "conforme_reach": True,
        "mention_danger": "H302 - Nocif en cas d ingestion",
        "equipements_protection": ["gants nitrile", "lunettes"],
    },
    {
        "produit": "Nettoyant HP vert dilution forte",
        "fournisseur": "EcoClean",
        "type_chimique": "biosorce",
        "numero_reach": "01-2119489385-27",
        "substances": ["alkyl polyglucoside", "acide citrique"],
        "cov_g_par_l": 0.3,
        "biodegradabilite_pct": 97.0,
        "ph": 7.1,
        "lc50_mg_l": 580.0,
        "ecolabel_eu": True,
        "conforme_reach": True,
        "mention_danger": "Aucune mention de danger",
        "equipements_protection": ["gants recommandes"],
    },
    {
        "produit": "Decapant sol industriel",
        "fournisseur": "IndustraNett",
        "type_chimique": "solvant",
        "numero_reach": "01-2119455851-35",
        "substances": ["naphta", "xylene", "ethylbenzene"],
        "cov_g_par_l": 145.0,
        "biodegradabilite_pct": 22.0,
        "ph": 8.1,
        "lc50_mg_l": 6.2,
        "ecolabel_eu": False,
        "conforme_reach": False,
        "mention_danger": "H304 - Peut etre mortel en cas d ingestion",
        "equipements_protection": ["gants nitrile", "lunettes", "masque", "combinaison"],
    },
]

def extract(output_path="data/fds_raw.csv"):
    print("[extract] Generation des donnees FDS simulees...")
    rows = []
    for fds in FDS_SIMULEES:
        rows.append({
            "produit":              fds["produit"],
            "fournisseur":          fds["fournisseur"],
            "type_chimique":        fds["type_chimique"],
            "numero_reach":         fds["numero_reach"],
            "substances":           ", ".join(fds["substances"]),
            "cov_g_par_l":          fds["cov_g_par_l"],
            "biodegradabilite_pct": fds["biodegradabilite_pct"],
            "ph":                   fds["ph"],
            "lc50_mg_l":            fds["lc50_mg_l"],
            "ecolabel_eu":          fds["ecolabel_eu"],
            "conforme_reach":       fds["conforme_reach"],
            "mention_danger":       fds["mention_danger"],
            "equipements_protection": ", ".join(fds["equipements_protection"]),
        })
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    df.to_csv(output_path, index=False)
    print("[extract] " + str(len(df)) + " fiches FDS generees -> " + output_path)
    return df, FDS_SIMULEES

def lire_pdf(pdf_path):
    texte = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texte += page.extract_text() or ""
    return texte

if __name__ == "__main__":
    df, _ = extract()
    print(df)
