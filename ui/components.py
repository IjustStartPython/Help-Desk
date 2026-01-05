import streamlit as st

def card(title, content_fn, height=None):
    """
    Crée une carte stylée pour le dashboard.
    title : titre de la carte
    content_fn : fonction qui affiche le contenu à l'intérieur
    height : hauteur optionnelle de la carte
    """
    style = f"""
    <div style="
        background-color: white;
        padding: 1.2rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 1.2rem;
        height: {height if height else 'auto'};
    ">
        <h4 style="margin-bottom: 0.8rem;">{title}</h4>
    """
    
    st.markdown(style, unsafe_allow_html=True)
    content_fn()  # Affiche ton contenu_________________________________
    st.markdown("</div>", unsafe_allow_html=True)  # Fermeture de la div_


def badge(text):
    st.markdown(
        f"""
        <span style="
            background-color:#E8F0FE;
            color:#1f4fd8;
            padding:4px 10px;
            border-radius:12px;
            margin-right:6px;
            font-size:0.85rem;
            display:inline-block;
        ">{text}</span>
        """,
        unsafe_allow_html=True
    )
