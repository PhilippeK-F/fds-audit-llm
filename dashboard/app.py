import streamlit as st
import pandas as pd
import plotly.express as px
import os
import subprocess

st.set_page_config(
    page_title="Audit FDS - Conformite Reglementaire",
    page_icon="📋",
    layout="wide"
)

@st.cache_data
def load_data():
    if not os.path.exists("data/fds_clean.csv"):
        return None
    return pd.read_csv("data/fds_clean.csv")

st.title("Audit de Conformité Réglementaire")
st.caption("Produits de nettoyage industriel — REACH / CLP / Écolabel EU")

if st.button("Relancer l'analyse complète"):
    with st.spinner("Analyse en cours..."):
        subprocess.run(["python", "run.py"])
    st.cache_data.clear()
    st.success("Analyse terminée !")

df = load_data()

if df is None:
    st.warning("Aucune donnée. Cliquez sur Relancer l'analyse.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Produits analysés",  len(df))
c2.metric("Conformes",          len(df[df["score_conformite"] >= 70]))
c3.metric("À surveiller",       len(df[(df["score_conformite"] >= 40) & (df["score_conformite"] < 70)]))
c4.metric("Critiques",          len(df[df["score_conformite"] < 40]))

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Score de conformité par produit")
    fig1 = px.bar(
        df.sort_values("score_conformite"),
        x="score_conformite",
        y="produit",
        orientation="h",
        color="score_conformite",
        color_continuous_scale="RdYlGn",
        range_color=[0, 100],
        labels={"score_conformite": "Score /100", "produit": ""}
    )
    fig1.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Répartition par niveau de risque")
    risque_count = df["niveau_risque"].value_counts().reset_index()
    risque_count.columns = ["niveau", "nb"]
    fig2 = px.pie(
        risque_count,
        names="niveau",
        values="nb",
        color="niveau",
        color_discrete_map={
            "Conforme": "#1D9E75",
            "Modere":   "#BA7517",
            "Critique": "#A32D2D"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Comparaison des indicateurs environnementaux")
fig3 = px.scatter(
    df,
    x="cov_g_par_l",
    y="biodegradabilite_pct",
    size="nb_alertes",
    color="niveau_risque",
    hover_name="produit",
    color_discrete_map={
        "Conforme": "#1D9E75",
        "Modere":   "#BA7517",
        "Critique": "#A32D2D"
    },
    labels={
        "cov_g_par_l":          "COV (g/L)",
        "biodegradabilite_pct": "Biodégradabilité (%)",
        "niveau_risque":        "Niveau"
    }
)
fig3.add_vline(x=30, line_dash="dash", line_color="orange", annotation_text="Seuil COV max")
fig3.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="Seuil biodég. min")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Détail des alertes par produit")
cols_alertes = ["produit", "score_conformite", "niveau_risque",
                "alerte_reach", "alerte_cov", "alerte_biodeg",
                "alerte_lc50", "alerte_ph", "nb_alertes"]
st.dataframe(
    df[cols_alertes].sort_values("score_conformite"),
    use_container_width=True,
    hide_index=True
)

if os.path.exists("data/rapports/audit_fds.pdf"):
    st.divider()
    st.subheader("Rapport PDF")
    with open("data/rapports/audit_fds.pdf", "rb") as f:
        st.download_button(
            label="Télécharger le rapport PDF",
            data=f,
            file_name="audit_fds_conformite.pdf",
            mime="application/pdf"
        )
