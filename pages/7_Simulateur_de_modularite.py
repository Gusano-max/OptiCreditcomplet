import streamlit as st
import math
from utils import calcul_mensualite
from style_utils import (
    configure_page, apply_custom_css, afficher_logo,
    ligne_decorative, encart_contact, format_nombre, afficher_resultats_markdown
)

configure_page(title="Simulateur de modularité", icon="🔄")
apply_custom_css()
afficher_logo()

st.markdown("<h3 style='text-align:center;'>Simulateur de modularité de prêt</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Rallongez ou réduisez la durée de votre prêt</h4>", unsafe_allow_html=True)
ligne_decorative()

# --- Saisie des données ---
capital = st.number_input("Capital restant dû (€)", min_value=1000.0, value=150000.0, step=1000.0, format="%.2f")
duree_restante = st.number_input("Durée restante (mois)", min_value=6, value=180, step=1)
taux = st.number_input("Taux hors assurance (% annuel)", min_value=0.1, value=3.0, step=0.1, format="%.2f")

type_modulation = st.selectbox("Type de modulation", ["Rallonger la durée", "Réduire la durée"])

# --- Sous-options conditionnelles ---
if type_modulation == "Rallonger la durée":
    rallongement = st.selectbox("Rallongement (mois)", [12, 24, 36])
else:
    augmentation_pct = st.selectbox("Augmentation de la mensualité", ["+10%", "+20%", "+30%"])

# --- Calculs ---
mensualite_actuelle = calcul_mensualite(capital, taux, duree_restante)
cout_total_actuel = mensualite_actuelle * duree_restante
interets_actuels = cout_total_actuel - capital

if type_modulation == "Rallonger la durée":
    nouvelle_duree = duree_restante + rallongement
    nouvelle_mensualite = calcul_mensualite(capital, taux, nouvelle_duree)
    cout_total_nouveau = nouvelle_mensualite * nouvelle_duree
    interets_nouveaux = cout_total_nouveau - capital
    surcout = cout_total_nouveau - cout_total_actuel

    resultats = (
        f"**📌 Mensualité actuelle :** {format_nombre(mensualite_actuelle)}<br>"
        f"**📌 Nouvelle mensualité (+{rallongement} mois) :** {format_nombre(nouvelle_mensualite)}<br>"
        f"**📌 Nouvelle durée :** {nouvelle_duree} mois ({nouvelle_duree // 12} ans et {nouvelle_duree % 12} mois)<br><br>"
        f"**💸 Coût total des intérêts avant modulation :** {format_nombre(interets_actuels)}<br>"
        f"**💸 Coût total des intérêts après modulation :** {format_nombre(interets_nouveaux)}<br>"
        f"**🔴 Surcoût total de la modulation :** {format_nombre(surcout)}"
    )
    afficher_resultats_markdown(resultats)

else:
    pct = int(augmentation_pct.replace("+", "").replace("%", "")) / 100
    nouvelle_mensualite = mensualite_actuelle * (1 + pct)
    taux_mensuel = taux / 100 / 12

    # Durée inverse : n = -ln(1 - C*r/M) / ln(1+r)
    ratio = capital * taux_mensuel / nouvelle_mensualite
    if ratio >= 1:
        st.error("🔴 La mensualité augmentée ne suffit pas à couvrir les intérêts. Modulation impossible.")
    else:
        nouvelle_duree = math.ceil(-math.log(1 - ratio) / math.log(1 + taux_mensuel))
        cout_total_nouveau = nouvelle_mensualite * nouvelle_duree
        interets_nouveaux = cout_total_nouveau - capital
        gain = cout_total_actuel - cout_total_nouveau

        resultats = (
            f"**📌 Mensualité actuelle :** {format_nombre(mensualite_actuelle)}<br>"
            f"**📌 Nouvelle mensualité ({augmentation_pct}) :** {format_nombre(nouvelle_mensualite)}<br>"
            f"**📌 Nouvelle durée :** {nouvelle_duree} mois ({nouvelle_duree // 12} ans et {nouvelle_duree % 12} mois)<br>"
            f"**📌 Réduction :** {duree_restante - nouvelle_duree} mois gagnés<br><br>"
            f"**💸 Coût total des intérêts avant modulation :** {format_nombre(interets_actuels)}<br>"
            f"**💸 Coût total des intérêts après modulation :** {format_nombre(interets_nouveaux)}<br>"
            f"**🟢 Gain total de la modulation :** {format_nombre(gain)}"
        )
        afficher_resultats_markdown(resultats)

encart_contact()
