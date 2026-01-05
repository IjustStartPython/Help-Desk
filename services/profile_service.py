import streamlit as st
from db.database import get_connection
from datetime import date

def render_profile_section():
    conn = get_connection()
    c = conn.cursor()

    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    date_naissance = st.date_input("Date de naissance")
    tdah = st.checkbox("Diagnostiqué TDAH")
    email = st.text_input("Email")

    if st.button("Enregistrer le profil"):
        c.execute('''INSERT OR REPLACE INTO user (id, nom, prenom, date_naissance, tdah, email)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (1, nom, prenom, date_naissance.isoformat(), tdah, email))
        conn.commit()
        st.success("Profil enregistré !")
