import streamlit as st
from services.chat_ai import chat_with_ai

def render_chat_section():
    """✅ Interface de chat améliorée"""
    st.markdown("### 💙 Mathi t'écoute")
    st.markdown("""
    Tu peux me parler de ce que tu ressens, de tes difficultés, de tes réussites...  
    Je suis là pour t'écouter sans jugement. 
    
    ⚠️ **Important** : Je ne remplace pas un professionnel de santé.
    """)
    
    # Initialisation de l'historique______________________________________________________
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    #Zone de messages_____________________________________________________________________
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for role, message in st.session_state.chat_history:
                if role == "Utilisateur":
                    st.chat_message("user").write(message)
                else:
                    st.chat_message("assistant", avatar="👩‍🦱").write(message)
        else:
            st.info("💬 Commence la conversation...")

    #Formulaire d'envoi__________________________________________________________________
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Ton message",
            placeholder="Écris ici...",
            height=100,
            key="chat_input"
        )
        
        col1, col2 = st.columns([4, 1])
        with col1:
            submitted = st.form_submit_button("📤 Envoyer", type="primary", use_container_width=True)
        with col2:
            clear = st.form_submit_button("🗑️ Effacer", use_container_width=True)

        if submitted and user_input.strip():
            #Ajouter le message utilisateur____________________________________________
            st.session_state.chat_history.append(("Utilisateur", user_input))
            
            #Obtenir la réponse de l'IA________________________________________________
            with st.spinner("Je réfléchis..."):
                response = chat_with_ai(user_input)
            
            #Ajouter la réponse________________________________________________________
            st.session_state.chat_history.append(("IA", response))
            st.rerun()
        
        if clear:
            st.session_state.chat_history = []
            st.rerun()


def render_chat_placeholder():
    """Version simplifiée pour le dashboard"""
    st.markdown("💙 **Besoin de parler ?**")
    st.markdown("Va dans l'onglet 'Mathi' pour discuter")