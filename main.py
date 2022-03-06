import functions as f
import streamlit as st


st.write("""
# Les eaux souterraines en France

Avec cette application web vous allez pouvoir extraire les niveaux piézométriques de plusieurs stations d'observations françaises
""")

code_postal = st.text_input('CODE POSTAL', '67000')

insee, ville, population = f.recup_commune(code_postal)

st.write(insee, ville, population)
