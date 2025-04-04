import streamlit as st
from datetime import datetime
from style_utils import (
    configure_page, apply_custom_css, afficher_logo, ligne_decorative, encart_contact,
    afficher_resultats_markdown, valider_entrees
)

configure_page(title="Simulation de capacité - Fourchette de taux", icon="📉")
apply_custom_css()
afficher_logo()

st.markdown("<h3 style='text-align:center;'>Calculette de capacité de financement</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Simulation avec une fourchette de taux</h4>", unsafe_allow_html=True)
ligne_decorative()

st.markdown("##### Informations personnelles et financières")
date_naissance = st.text_input("Date de naissance (JJ/MM/AAAA)", "")
revenus_salariaux = st.number_input("Revenus salariaux (€)", min_value=0.0, format="%.2f")
revenus_locatifs = st.number_input("Revenus locatifs (seront pondérés à 70%)", min_value=0.0, format="%.2f")
mensualite_credit_en_cours = st.number_input("Mensualité de crédits en cours (€)", min_value=0.0, format="%.2f")

st.markdown("##### Paramètres de simulation")
duree_choisie = st.number_input("Durée souhaitée du crédit (en années)", min_value=1, max_value=35, value=25)
taux_choisi = st.number_input("Taux d'intérêt souhaité (%)", min_value=0.1, step=0.01, format="%.2f")

if st.button("Calculer"):
    champs = {
        "revenus_salariaux": revenus_salariaux,
        "revenus_locatifs": revenus_locatifs,
        "mensualite_credit_en_cours": mensualite_credit_en_cours,
        "duree_choisie": duree_choisie,
        "taux_choisi": taux_choisi
    }

    regles = {
        "revenus_salariaux": (100, 1_000_000, "Les revenus salariaux"),
        "revenus_locatifs": (0, 1_000_000, "Les revenus locatifs"),
        "mensualite_credit_en_cours": (0, 20_000, "Les mensualités actuelles"),
        "duree_choisie": (1, 35, "La durée du crédit"),
        "taux_choisi": (0.1, 10, "Le taux")
    }

    erreurs = valider_entrees(champs, regles)

    try:
        naissance = datetime.strptime(date_naissance, "%d/%m/%Y")
    except ValueError:
        erreurs.append("📅 La date de naissance est invalide (format attendu : JJ/MM/AAAA)")

    if erreurs:
        for e in erreurs:
            st.error(e)
    else:
        try:
            age = (datetime.today() - naissance).days // 365
            taux_assurance = 0.25 / 100 / 12 if age < 30 else 0.35 / 100 / 12 if age <= 50 else 0.50 / 100 / 12
            mensualite_max = (revenus_salariaux + 0.7 * revenus_locatifs) * 0.35 - mensualite_credit_en_cours

            resultats = f"**💳 Mensualité maximale (assurance incluse)** : {mensualite_max:,.2f} €\n\n"
            taux_list = [round(taux_choisi - 0.30, 2), taux_choisi, round(taux_choisi + 0.30, 2)]
            duree_mois = int(duree_choisie * 12)

            for taux in taux_list:
                taux_mensuel = taux / 100 / 12
                montant_emprunte = 0
                montant_test = 100000

                while True:
                    mensualite_emprunt = montant_test * ((taux_mensuel * (1 + taux_mensuel) ** duree_mois) /
                                                         ((1 + taux_mensuel) ** duree_mois - 1))
                    assurance_mensuelle = montant_test * taux_assurance
                    mensualite_totale = mensualite_emprunt + assurance_mensuelle
                    if mensualite_totale > mensualite_max:
                        break
                    montant_emprunte = montant_test
                    montant_test += 1000

                mensualite_emprunt_final = montant_emprunte * ((taux_mensuel * (1 + taux_mensuel) ** duree_mois) /
                                                               ((1 + taux_mensuel) ** duree_mois - 1))
                assurance_mensuelle_final = montant_emprunte * taux_assurance
                mensualite_totale_final = mensualite_emprunt_final + assurance_mensuelle_final

                interets_totaux = mensualite_emprunt_final * duree_mois - montant_emprunte
                assurance_totale = assurance_mensuelle_final * duree_mois

                resultats += (
                    f"### 🔍 Résultat pour un taux de {taux:.2f}%\n"
                    f"- 💰 Montant empruntable : **{montant_emprunte:,.2f} €**\n"
                    f"- 📉 Mensualité sans assurance : **{mensualite_emprunt_final:,.2f} €**\n"
                    f"- 🛡️ Mensualité avec assurance : **{mensualite_totale_final:,.2f} €**\n"
                    f"- 💸 Coût total des intérêts : **{interets_totaux:,.2f} €**\n"
                    f"- 🧾 Coût total de l’assurance : **{assurance_totale:,.2f} €**\n\n"
                )

            afficher_resultats_markdown(resultats)

        except Exception:
            st.error("🛑 Erreur 500 – Une erreur interne est survenue. Veuillez réessayer.")

encart_contact()
