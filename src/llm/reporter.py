import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from datetime import datetime

COULEURS = {
    "Conforme":  HexColor("#1D9E75"),
    "Modere":    HexColor("#BA7517"),
    "Critique":  HexColor("#A32D2D"),
    "header":    HexColor("#1A1A2E"),
    "gris_clair":HexColor("#F5F5F5"),
}

def generer_rapport(resultats, output_path="data/rapports/audit_fds.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    style_titre = ParagraphStyle(
        "titre",
        parent=styles["Title"],
        fontSize=20,
        textColor=COULEURS["header"],
        spaceAfter=6
    )
    style_sous_titre = ParagraphStyle(
        "sous_titre",
        parent=styles["Normal"],
        fontSize=11,
        textColor=HexColor("#666666"),
        spaceAfter=20
    )
    style_h2 = ParagraphStyle(
        "h2",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=COULEURS["header"],
        spaceBefore=16,
        spaceAfter=8
    )
    style_h3 = ParagraphStyle(
        "h3",
        parent=styles["Heading3"],
        fontSize=11,
        textColor=COULEURS["header"],
        spaceBefore=10,
        spaceAfter=4
    )
    style_normal = ParagraphStyle(
        "normal",
        parent=styles["Normal"],
        fontSize=9,
        leading=14,
        spaceAfter=6
    )

    elements = []

    # En-tete
    elements.append(Paragraph("Audit de Conformite Reglementaire", style_titre))
    elements.append(Paragraph(
        "Produits de nettoyage industriel — REACH / CLP / Ecolabel EU — " +
        datetime.now().strftime("%d/%m/%Y"),
        style_sous_titre
    ))

    # Tableau de synthese
    elements.append(Paragraph("Synthese des resultats", style_h2))

    data_table = [["Produit", "Fournisseur", "Score", "Niveau"]]
    for r in resultats:
        couleur = COULEURS.get(r["niveau_risque"], black)
        data_table.append([
            r["produit"][:35],
            r.get("fournisseur", "-"),
            str(r["score_conformite"]) + "/100",
            r["niveau_risque"]
        ])

    table = Table(data_table, colWidths=[7*cm, 4*cm, 2.5*cm, 2.5*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  COULEURS["header"]),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  white),
        ("FONTSIZE",      (0, 0), (-1, 0),  9),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [COULEURS["gris_clair"], white]),
        ("FONTSIZE",      (0, 1), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 0.3, HexColor("#CCCCCC")),
        ("ALIGN",         (2, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))

    # Analyses detaillees
    elements.append(Paragraph("Analyses detaillees par produit", style_h2))

    for r in resultats:
        couleur = COULEURS.get(r["niveau_risque"], black)

        elements.append(Paragraph(
            r["produit"] + " — " + r["niveau_risque"] + " (" + str(r["score_conformite"]) + "/100)",
            style_h3
        ))

        if r.get("analyse_llm"):
            for ligne in r["analyse_llm"].split("\n"):
                if ligne.strip():
                    elements.append(Paragraph(ligne.strip(), style_normal))

        elements.append(Spacer(1, 0.3*cm))

    doc.build(elements)
    print("[reporter] Rapport genere -> " + output_path)
    return output_path

if __name__ == "__main__":
    resultats_test = [
        {
            "produit": "Degraissant solvant chlore HD",
            "fournisseur": "ChemPro",
            "score_conformite": 25,
            "niveau_risque": "Critique",
            "analyse_llm": "Test de generation du rapport PDF.\nCe produit presente des non-conformites majeures.\n1. RESUME : Produit non conforme REACH.\n2. NON-CONFORMITES : COV eleve, biodegradabilite faible.\n3. RISQUES : Impact environnemental eleve.\n4. RECOMMANDATIONS : Remplacer par alternative biosourcee.\n5. CONCLUSION : Remplacement urgent recommande."
        },
        {
            "produit": "Degraissant biosorce CitraClean",
            "fournisseur": "VerteChimie",
            "score_conformite": 100,
            "niveau_risque": "Conforme",
            "analyse_llm": "Produit conforme a toutes les reglementations.\n1. RESUME : Excellent profil environnemental.\n2. NON-CONFORMITES : Aucune.\n3. RISQUES : Minimaux.\n4. RECOMMANDATIONS : Maintenir ce produit.\n5. CONCLUSION : Produit recommande."
        }
    ]
    generer_rapport(resultats_test)
