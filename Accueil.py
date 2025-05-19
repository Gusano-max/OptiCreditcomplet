import streamlit as st
import numpy as np
from style_utils import configure_page, apply_custom_css, afficher_logo, ligne_decorative, encart_contact, titre_avec_ligne


configure_page(title="Simulation de rachat de prêt", icon="📉")
apply_custom_css()
afficher_logo()


st.markdown("""
    <h2 style='text-align: center; color: #31331F; margin-bottom: 1.5px;'>
        Bienvenue sur OptiCrédit 💼
    </h2>
    <h3 style='text-align: center; color: #31331F; margin-top: -1.5px'>
        Votre boîte à outils du financement immobilier développée par Nicolas Galan
    </h3>
""", unsafe_allow_html=True)


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

ligne_decorative()

st.write("---")

st.markdown("""
### 📍 Ce que vous pouvez faire ici et en toute autonomie :
- 🧮 Utiliser les **Calculettes de capacité d’emprunt en fonction de vos revenus et de vos charges**
- 🧮 Calculer une **mensualité** à partir d'un **capital emprunté**
- 🧮 Calculer un **capital empruntable** à partir **d'une mensualité*** 
- 🔁 Simuler un **rachat de crédit**
- 🔁 Simuler un **différé partiel ou total**                       

👉 Sélectionnez une section dans la barre latérale à gauche pour commencer.
""")



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
    📬 DM sur X via <a href="https://twitter.com/gusano197" target="_blank" style="color:#C32026; text-decoration:none; font-weight:bold;">@gusano197</a>
    ou ✉️ <a href="mailto:nicolas.galan@talan-patrimoine.fr" style="color:#C32026; text-decoration:none; font-weight:bold;">nicolas.galan@talan-patrimoine.fr</a>
</div>
""", unsafe_allow_html=True)

