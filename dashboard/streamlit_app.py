import pandas as pd
import streamlit as st

# TODO: remplacer les données fictives par une vraie source
# Exemples :
# - Lire depuis PostgreSQL :
#     from sqlalchemy import create_engine
#     import os
#     engine = create_engine(...)
#     df = pd.read_sql("SELECT * FROM nom_table", engine)
#
# - Lire depuis un CSV :
#     df = pd.read_csv("data/output.csv")

st.title("Data Engineering Dashboard")

# TODO: adapter le titre et la description à ton projet
st.markdown("Vue d'ensemble des données traitées par le pipeline ETL.")

# Données fictives — à remplacer
df = pd.DataFrame({
    "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "value": [10, 30, 20],
})

# TODO: adapter les graphiques à tes données
st.subheader("Évolution de la valeur")
st.line_chart(df.set_index("date"))

st.subheader("Données brutes")
st.dataframe(df)
