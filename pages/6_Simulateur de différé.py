import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import tempfile
from utils import calcul_mensualite, calcul_assurance_mensuelle, get_taux_assurance
from style_utils import (
    configure_page, apply_custom_css, afficher_resultats_markdown, afficher_logo,
    ligne_decorative, encart_contact, titre_avec_ligne, valider_entrees, format_nombre
)
from fpdf import FPDF

apply_custom_css()
afficher_logo()

st.markdown("<h3 style='text-align:center;'>Simulateur de différé partiel ou total</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Calculez le coût de votre différé d'amortissement</h3>", unsafe_allow_html=True)
ligne_decorative()

# --- Saisie des données utilisateur ---
col1, col2 = st.columns(2)

with col1:
    montant = st.number_input("Montant du prêt (€)", min_value=1000.0, value=300000.0, step=1000.0, format="%0.2f")
    duree_amortissement = st.number_input("Durée totale du prêt (mois)", min_value=12, value=300, step=12)
    duree_differe = st.number_input("Durée du différé (mois)", min_value=0, max_value=60, value=24)
    taux = st.number_input("Taux d'intérêt annuel (%)", min_value=0.1, value=3.3, step=0.1, format="%0.2f")

with col2:
    date_naissance = st.date_input("Date de naissance de l'emprunteur", value=datetime(1985, 1, 1))
    taux_assurance = get_taux_assurance(date_naissance)
    st.markdown(f"**Taux d'assurance estimé : {taux_assurance:.2f} %**")

    type_differe = st.radio("Type de différé", ["Partiel", "Total"])
    mode_differe = st.radio("Mode de différé", ["Inclus dans la durée", "Ajouté à la durée"])

# --- Mensualité sans différé ---
mensualite_sans_differe = calcul_mensualite(montant, taux, duree_amortissement)
assurance_mensuelle = calcul_assurance_mensuelle(montant, taux_assurance)

# --- Calculs complets avant affichage des résultats ---

# Durée d'amortissement effective
if mode_differe == "Inclus dans la durée":
    duree_remboursement = duree_amortissement - duree_differe
else:
    duree_remboursement = duree_amortissement

# --- Déblocages pendant différé (max 10 paliers) ---
deblocages = []
nb_paliers = st.slider("Nombre de déblocages pendant le différé", 1, 10, 5)
cols = st.columns(nb_paliers)
total_pourcent = 0

for i in range(nb_paliers):
    with cols[i]:
        pourcent = st.number_input(f"Palier {i+1} (%)", min_value=0.0, max_value=100.0, value=0.0, key=f"p{i}")
        deblocages.append(pourcent)
        total_pourcent += pourcent

if total_pourcent == 100:
    # Répartition des mois par palier basée sur les %
    mois_par_palier_list = []
    mois_total = 0
    for i in range(nb_paliers):
        mois = round(duree_differe * (deblocages[i] / 100))
        mois_par_palier_list.append(mois)
        mois_total += mois
    ecart = duree_differe - mois_total
    for i in range(abs(ecart)):
        idx = i % nb_paliers
        mois_par_palier_list[idx] += 1 if ecart > 0 else -1
    assert sum(mois_par_palier_list) == duree_differe, "Erreur de répartition du différé."

    interets_total_differe = 0
    tableau_amort = []
    capital_cumule = 0
    taux_mensuel = taux / 100 / 12
    mois_courant = 1
    interets_cumules = 0

    for i in range(nb_paliers):
        mois_palier = mois_par_palier_list[i]
        capital_cumule = montant * sum(deblocages[:i+1]) / 100
        interets = capital_cumule * taux_mensuel
        mensualite = interets + assurance_mensuelle if type_differe == "Partiel" else assurance_mensuelle

        for m in range(mois_palier):
            interets_courant = interets if type_differe == "Partiel" else 0
            interets_cumules += interets_courant
            tableau_amort.append({
                "Mois": mois_courant,
                "Phase": "Différé",
                "Capital restant dû (€)": capital_cumule,
                "Intérêts (€)": interets_courant,
                "Amortissement (€)": 0,
                "Assurance (€)": assurance_mensuelle,
                "Mensualité (€)": mensualite,
                "Intérêts cumulés (€)": interets_cumules
            })
            mois_courant += 1

        if type_differe == "Partiel":
            interets_total_differe += interets * mois_palier

    if type_differe == "Total":
        interets_total_differe = montant * taux_mensuel * duree_differe
        montant_final = montant + interets_total_differe
    else:
        montant_final = montant

    mensualite_apres_differe_hors_assurance = calcul_mensualite(montant_final, taux, duree_remboursement)
    mensualite_apres_differe = mensualite_apres_differe_hors_assurance + assurance_mensuelle

    interets_post_differe = (mensualite_apres_differe_hors_assurance * duree_remboursement) - montant_final
    cout_total = interets_total_differe + interets_post_differe + (assurance_mensuelle * (duree_remboursement + duree_differe))

    capital = montant_final
    for mois in range(1, duree_remboursement + 1):
        interet = capital * taux_mensuel
        principal = mensualite_apres_differe_hors_assurance - interet
        capital_restant = capital - principal
        interets_cumules += interet
        tableau_amort.append({
            "Mois": mois_courant,
            "Phase": "Amortissement",
            "Capital restant dû (€)": capital,
            "Intérêts (€)": interet,
            "Amortissement (€)": principal,
            "Assurance (€)": assurance_mensuelle,
            "Mensualité (€)": mensualite_apres_differe,
            "Intérêts cumulés (€)": interets_cumules
        })
        capital = capital_restant
        mois_courant += 1

    st.subheader("📈 Résultats")
    st.write(f"**Mensualité sans différé (hors assurance) :** {format_nombre(mensualite_sans_differe)}")
    st.write(f"**Prime d'assurance mensuelle :** {format_nombre(assurance_mensuelle)}")
    st.write(f"**Mensualité après le différé :** {format_nombre(mensualite_apres_differe)} (dont {format_nombre(assurance_mensuelle)} d'assurance)")

    if type_differe == "Partiel":
        st.write(f"**Coût total du différé partiel (intérêts versés) :** {format_nombre(interets_total_differe)}")
    elif type_differe == "Total":
        st.write(f"**Coût du différé total (intérêts capitalisés) :** {format_nombre(interets_total_differe)}")

    st.write(f"**Coût total estimé du crédit avec différé :** {format_nombre(cout_total)}")

    df_final = pd.DataFrame(tableau_amort)
    st.subheader("📅 Tableau d'amortissement complet")
    colonnes_montants = [
      "Capital restant dû (€)", "Intérêts (€)", "Amortissement (€)",
      "Assurance (€)", "Mensualité (€)", "Intérêts cumulés (€)"
    ]
    for col in colonnes_montants:
        df_final[col] = df_final[col].apply(format_nombre)

    st.dataframe(df_final, use_container_width=True)

    # Export PDF
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Tableau d'amortissement", ln=True, align="C")

        def chapter_table(self, title, dataframe):
            self.ln(10)
            self.set_font("Arial", "B", 11)
            self.cell(0, 10, title, ln=True)
            self.set_font("Arial", "", 8)
            col_widths = [30] * len(dataframe.columns)
            for i, col in enumerate(dataframe.columns):
                header = str(col).encode('latin-1', 'replace').decode('latin-1')
                self.cell(col_widths[i], 8, header, border=1)
            self.ln()
            for _, row in dataframe.iterrows():
                for i, item in enumerate(row):
                    val = round(item, 2) if isinstance(item, (int, float, np.number)) else str(item)
                    val = str(val).encode('latin-1', 'replace').decode('latin-1')
                    self.cell(col_widths[i], 8, val, border=1)
                self.ln()

    if st.button("📄 Exporter le tableau en PDF"):
        pdf = PDF(orientation='L', format='A4') 
        pdf.add_page()
        pdf.chapter_table("Tableau d'amortissement complet", df_final)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
            pdf.output(tmpfile.name)
            with open(tmpfile.name, "rb") as f:
                st.download_button("📥 Télécharger le PDF", f, file_name="amortissement.pdf", mime="application/pdf")
