import streamlit as st

def configure_page(title="OptiCrédit", icon="💼"):
    st.set_page_config(page_title=title, page_icon=icon, layout="centered")

def format_nombre(valeur):
    return "{:,.2f} €".format(valeur).replace(",", " ").replace(".", ",")

def apply_custom_css():
    st.markdown("""
        <style>
        html, body, .stApp {
            background-color: #F4F4F4 !important;
            color: #000000 !important;
            font-family: "Arial", sans-serif;
        }

        /* Inputs champs */
        input, textarea, .stNumberInput input {
            border: none;
            background-color: #d7dbdd !important;
            border-radius: 8px;
            padding: 8px;
            color: #000000 !important;
        }
        input:focus, textarea:focus {
            outline: none;
            border: none;
            box-shadow: 0 0 0 2px #C32026;
            background-color: #FFFFFF !important;
        }

        /* Boutons rouges */
        .stButton>button {
            background-color: #C32026 !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            padding: 10px 24px;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #a91b1f !important;
        }
        </style>
    """, unsafe_allow_html=True)

def titre_avec_ligne(titre: str):
    """Affiche un titre centré avec ligne décorative rouge."""
    st.markdown(f"<h2 style='text-align: center;'>{titre}</h2>", unsafe_allow_html=True)
    ligne_decorative()


def ligne_decorative():
    st.markdown("""
        <div style="
            width: 100%;
            height: 5px;
            background: linear-gradient(to right, rgba(195,32,38,0), #C32026, rgba(195,32,38,0));
            border-radius: 5px;
            margin-top: -5px;
            margin-bottom: 15px;
        "></div>
    """, unsafe_allow_html=True)

def afficher_resultats_markdown(texte: str):
    """Affiche un bloc de texte Markdown stylisé sans encart coloré."""
    st.markdown(f"""
        <div style='
            background-color: #d7dbdd;
            border: 1px solid #C32026;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
        '>
            {texte}
    """, unsafe_allow_html=True)

def afficher_resultats_markdown(texte_markdown):
    """Affiche un encadré sobre et élégant contenant du Markdown."""
    st.markdown(f"""
        <div style='
            background-color: #d7dbdds;
            border: 1px solid #C32026;
            padding: 1rem;
            border-radius: 10px;
            font-size: 16px;
            color: #000;
        '>
            {texte_markdown}
        </div>
    """, unsafe_allow_html=True)


def encart_contact():
    st.markdown("""
    <div style="
        border: 1px solid #C32026;
        background-color: #F5F5F5;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: #000000;
        font-size: 16px;
        margin-top: 30px;
        line-height: 1.6;
    ">
        📩 <strong>Pour plus de renseignements, contactez-moi !</strong><br><br>
        📬 DM via <a href="https://twitter.com/gusano197" target="_blank" style="color:#C32026; text-decoration:none; font-weight:bold;">@gusano197</a>
        ou ✉️ <a href="mailto:nicolas.galan@talan-patrimoine.fr" style="color:#C32026; text-decoration:none; font-weight:bold;">nicolas.galan@talan-patrimoine.fr</a>
    </div>
    """, unsafe_allow_html=True)


def afficher_logo():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.webp", width="stretch")

def valider_entrees(valeurs, regles):
    """Vérifie chaque champ selon les règles fournies. Retourne une liste d'erreurs."""
    erreurs = []
    for champ, valeur in valeurs.items():
        if champ in regles:
            minimum, maximum, label = regles[champ]
            if not (minimum <= valeur <= maximum):
                erreurs.append(f"🔴 {label} doit être entre {minimum} et {maximum}")
    return erreurs



