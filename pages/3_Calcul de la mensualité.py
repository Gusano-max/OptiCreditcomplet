import streamlit as st
import pandas as pd
import numpy as np
import io 
import math
from style_utils import configure_page, apply_custom_css, afficher_logo, ligne_decorative, encart_contact, titre_avec_ligne

configure_page(title="Capacité de financement", icon="📊")
apply_custom_css()
afficher_logo()

st.markdown("<h3 style='text-align:center;'>Calculer une mensualité</h3>", unsafe_allow_html=True)
ligne_decorative() 

def format_nombre(valeur):
    return "{:,.2f} €".format(valeur).replace(",", " ").replace(".", ",")
    

def generer_amortissement(montant, taux_annuel, duree_mois):
    taux_mensuel = taux_annuel / 12 / 100
    mensualite = (montant * taux_mensuel) / (1 - (1 + taux_mensuel) ** -duree_mois)
    capital_restant = montant
    amortissement = []
    for mois in range(1, duree_mois + 1):
        interets = capital_restant * taux_mensuel
        capital_rembourse = mensualite - interets
        capital_restant -= capital_rembourse
        amortissement.append((mois, round(capital_restant, 2), round(interets, 2), round(capital_rembourse, 2), round(mensualite, 2)))
    return amortissement

st.subheader("Informations sur le Prêt")
montant = st.number_input("Montant à emprunter (€)", min_value=0.1, value=100000., step=0.1)
taux_principal = st.number_input("Taux du prêt principal (%)", min_value=0.1, value=2.5, step=0.1)
taux_mensuel = taux_principal / 12 / 100
duree_mois_principal = st.number_input("Durée du prêt principal (mois)", min_value=12, max_value=360, value=240)
mensualite_credit = (montant * taux_mensuel) / (1 - (1 + taux_mensuel) ** (-duree_mois_principal))


st.write("---")
st.subheader("🏠 Détails du prêt Principal")
st.write(f"Montant du prêt principal : {format_nombre(montant)}")
st.write(f"Durée : {duree_mois_principal} mois")
st.write(f"Mensualité hors assurance : {format_nombre(mensualite_credit)}")
interets_total = mensualite_credit * duree_mois_principal - montant
st.write(f"💸 Coût total des intérêts : {format_nombre(interets_total)}")

encart_contact()
