import streamlit as st
from style_utils import configure_page, apply_custom_css, afficher_logo, ligne_decorative, encart_contact

configure_page(title="Capacité de financement", icon="📊")
apply_custom_css()


st.markdown("<h3 style='text-align:center;'>Calculer un capital à emprunter à partir d'une mensualité</h3>", unsafe_allow_html=True)
ligne_decorative()


def format_nombre(valeur):
    return "{:,.2f} €".format(valeur).replace(",", " ").replace(".", ",")


st.subheader("Données de simulation")

mensualite = st.number_input("Mensualité souhaitée (€)", min_value=100.0, step=50.0, value=1000.0)
taux_annuel = st.number_input("Taux d’emprunt (%)", min_value=0.1, step=0.1, value=2.5)
duree_mois = st.number_input("Durée du prêt (en mois)", min_value=12, max_value=360, step=12, value=240)

# Calcul
taux_mensuel = taux_annuel / 12 / 100

if taux_mensuel > 0:
    capital_empruntable = mensualite * (1 - (1 + taux_mensuel) ** -duree_mois) / taux_mensuel
else:
    capital_empruntable = mensualite * duree_mois  # prêt à taux 0

total_rembourse = mensualite * duree_mois
interets_total = total_rembourse - capital_empruntable


# Résultat
st.write("---")
st.subheader("📊 Résultat")
st.write(f"💰 Capital empruntable : **{format_nombre(capital_empruntable)}**")
st.write(f"📅 Durée : {duree_mois} mois")
st.write(f"💸 Coût total des intérêts : {format_nombre(interets_total)}")

encart_contact()


