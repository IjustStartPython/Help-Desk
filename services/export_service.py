import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF
from datetime import datetime

def render_export_section():
    """✅ CORRIGÉ : utilise les vraies tables de la base de données"""
    st.header("📥 Export de tes données")

    st.markdown("""
    Tu peux exporter toutes tes données pour :
    - Les sauvegarder
    - Les analyser ailleurs
    - Les partager avec un professionnel de santé

    **🔒 Note de confidentialité :** Tes données sont stockées localement et chiffrées sur ton appareil.
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Exporter en Excel", type="primary", use_container_width=True):
            export_to_excel()

    with col2:
        if st.button("📄 Exporter en PDF", type="primary", use_container_width=True):
            export_to_pdf()


def export_to_excel():
    """Exporte les données en Excel"""
    try:
        conn = st.session_state.conn

        #Lecture des données depuis les vraies tables__________________________________________________________
        df_mood = pd.read_sql("SELECT * FROM mood ORDER BY created_at DESC", conn)
        df_tasks = pd.read_sql("SELECT * FROM tasks ORDER BY created_at DESC", conn)
        df_notes = pd.read_sql("SELECT * FROM notes ORDER BY created_at DESC", conn)
        df_users = pd.read_sql("SELECT * FROM users", conn)

        #Création du fichier Excel en mémoire___________________________________________________________________
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_mood.to_excel(writer, sheet_name="Humeurs", index=False)
            df_tasks.to_excel(writer, sheet_name="Tâches", index=False)
            df_notes.to_excel(writer, sheet_name="Notes", index=False)
            df_users.to_excel(writer, sheet_name="Profil", index=False)

        output.seek(0)

        #Téléchargement_________________________________________________________________________________________
        st.download_button(
            label="⬇️ Télécharger Excel",
            data=output,
            file_name=f"donnees_helpdesk_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel"
        )

        st.success("✅ Export Excel prêt ! Clique sur le bouton ci-dessus.")

    except Exception as e:
        st.error(f"❌ Erreur lors de l'export Excel : {str(e)}")


def export_to_pdf():
    """Exporte les données en PDF formaté pour un professionnel de santé"""
    try:
        conn = st.session_state.conn

        #Récupération des données______________________________________________________________________________
        profile = pd.read_sql("SELECT * FROM users ORDER BY id DESC LIMIT 1", conn)
        moods = pd.read_sql("SELECT * FROM mood ORDER BY created_at DESC", conn)
        tasks = pd.read_sql("SELECT * FROM tasks ORDER BY created_at DESC LIMIT 50", conn)
        notes = pd.read_sql("SELECT * FROM notes ORDER BY created_at DESC LIMIT 30", conn)

        #Création du PDF_______________________________________________________________________________________
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        #Titre___________________________________________________________________________________________________
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Rapport de suivi - Help-Desk", ln=True, align="C")
        pdf.ln(5)

        #Date du rapport_________________________________________________________________________________________
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Date du rapport : {datetime.now().strftime('%d/%m/%Y')}", ln=True)
        pdf.ln(5)

        #Informations du profil___________________________________________________________________________________
        if not profile.empty:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Informations du profil", ln=True)
            pdf.set_font("Arial", "", 10)

            prenom = profile.iloc[0]['prenom']
            birth_date = profile.iloc[0]['birth_date']
            tags = profile.iloc[0]['tags']

            pdf.cell(0, 6, f"Prenom : {prenom}", ln=True)
            pdf.cell(0, 6, f"Date de naissance : {birth_date}", ln=True)
            pdf.cell(0, 6, f"Informations : {tags}", ln=True)
            pdf.ln(8)

        #Statistiques générales________________________________________________________________________________________
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Statistiques", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, f"Nombre d'humeurs enregistrees : {len(moods)}", ln=True)
        pdf.cell(0, 6, f"Nombre de taches creees : {len(tasks)}", ln=True)
        pdf.cell(0, 6, f"Nombre de notes : {len(notes)}", ln=True)
        pdf.ln(8)

        #Évolution de l'humeur__________________________________________________________________________________________
        if not moods.empty:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Evolution de l'humeur", ln=True)
            pdf.set_font("Arial", "", 10)

            avg_mood = moods['mood_value'].mean()
            max_mood = moods['mood_value'].max()
            min_mood = moods['mood_value'].min()

            pdf.cell(0, 6, f"Humeur moyenne : {avg_mood:.1f}/10", ln=True)
            pdf.cell(0, 6, f"Humeur maximale : {max_mood}/10", ln=True)
            pdf.cell(0, 6, f"Humeur minimale : {min_mood}/10", ln=True)
            pdf.ln(8)

            #Dernières humeurs_________________________________________________________________________________________
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Dernieres humeurs enregistrees (10 plus recentes)", ln=True)
            pdf.set_font("Arial", "", 9)

            for idx, row in moods.head(10).iterrows():
                date_str = row['created_at'][:10] if pd.notna(row['created_at']) else "N/A"
                mood_val = row['mood_value']
                emotion = row['emotion'] if pd.notna(row['emotion']) else "Non specifie"
                motivation = row['motivation'] if pd.notna(row['motivation']) else "Non specifie"

                pdf.set_font("Arial", "B", 9)
                pdf.cell(0, 5, f"{date_str} - Humeur : {mood_val}/10", ln=True)
                pdf.set_font("Arial", "", 9)
                pdf.cell(0, 5, f"  Emotion : {emotion[:60]}", ln=True)
                pdf.cell(0, 5, f"  Motivation : {motivation[:60]}", ln=True)

                if pd.notna(row['notes']) and row['notes']:
                    notes_text = row['notes'][:100]
                    pdf.cell(0, 5, f"  Notes : {notes_text}...", ln=True)
                pdf.ln(2)

        pdf.add_page()

        #Notes récentes______________________________________________________________________________________________________
        if not notes.empty:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Notes recentes", ln=True)
            pdf.set_font("Arial", "", 9)

            for idx, row in notes.head(20).iterrows():
                date_str = row['created_at'][:16] if pd.notna(row['created_at']) else "N/A"
                content = row['content'] if pd.notna(row['content']) else ""

                pdf.set_font("Arial", "B", 9)
                pdf.cell(0, 5, f"{date_str}", ln=True)
                pdf.set_font("Arial", "", 9)

                #Découper le texte si trop long_______________________________________________________________________________
                if len(content) > 150:
                    content = content[:150] + "..."

                pdf.multi_cell(0, 5, content)
                pdf.ln(2)

        #Générer le PDF_______________________________________________________________________________________________________
        pdf_output = BytesIO()
        pdf_content = pdf.output()
        pdf_output.write(pdf_content)
        pdf_output.seek(0)

        #Téléchargement_________________________________________________________________________________________________________
        st.download_button(
            label="⬇️ Télécharger PDF",
            data=pdf_output,
            file_name=f"rapport_helpdesk_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            key="download_pdf"
        )

        st.success("✅ Export PDF prêt ! Clique sur le bouton ci-dessus.")

    except Exception as e:
        st.error(f"❌ Erreur lors de l'export PDF : {str(e)}")


def show_data_stats():
    """Affiche des statistiques sur les données"""
    conn = st.session_state.conn
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mood_count = pd.read_sql("SELECT COUNT(*) as count FROM mood", conn).iloc[0]['count']
        st.metric("Humeurs enregistrées", mood_count)
    
    with col2:
        task_count = pd.read_sql("SELECT COUNT(*) as count FROM tasks", conn).iloc[0]['count']
        st.metric("Tâches créées", task_count)
    
    with col3:
        note_count = pd.read_sql("SELECT COUNT(*) as count FROM notes", conn).iloc[0]['count']
        st.metric("Notes prises", note_count)