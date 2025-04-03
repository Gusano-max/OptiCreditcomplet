
import streamlit as st
from style_utils import configure_page, apply_custom_css, afficher_logo, ligne_decorative, encart_contact, titre_avec_ligne


configure_page(title="Simulation de rachat de prêt", icon="📉")
apply_custom_css()
afficher_logo()


st.markdown("<h3 style='text-align:center;'>Calculette de capacité de financement</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Calculez votre capacité d'emprunt avec une fourchette de taux</h3>", unsafe_allow_html=True)
ligne_decorative()


st.markdown("##### Informations personnelles et financières")
date_naissance = st.text_input("Date de naissance (JJ/MM/AAAA)", "")
revenus_salariaux = st.number_input("Revenus salariaux (€)", min_value=0.0, format="%.2f")
revenus_locatifs = st.number_input("Revenus locatifs (seront pondérés automatiquement à 70%)", min_value=0.0, format="%.2f")
mensualite_credit_en_cours = st.number_input("Mensualité de crédits en cours (€)", min_value=0.0, format="%.2f")

st.markdown("##### Taux d'intérêt annuels")
duree_choisie = st.number_input("Durée souhaitée du crédit (en années)", min_value=1, max_value=30, value=25)
taux_choisi = st.number_input("Taux d'intérêt souhaité (%)", min_value=0.0, step=0.01, format="%.2f")

if st.button("Calculer"):
    from datetime import datetime

    # Validation de la date
    try:
        naissance = datetime.strptime(date_naissance, "%d/%m/%Y")
    except ValueError:
        st.error("Veuillez entrer une date valide au format JJ/MM/AAAA")
    else:
        # Calcul de l'âge
        age = (datetime.today() - naissance).days // 365
        
        # Définir le taux d’assurance en fonction de l'âge
        if age < 30:
            taux_assurance = 0.25 / 100 / 12
        elif age <= 50:
            taux_assurance = 0.35 / 100 / 12
        else:
            taux_assurance = 0.50 / 100 / 12

        mensualite_max = (revenus_salariaux + 0.7 * revenus_locatifs) * 0.35 - mensualite_credit_en_cours

        st.markdown(f"**💳 Mensualité maximale (assurance incluse)** : {mensualite_max:,.2f} €")

        # Taux à tester
        taux_list = [taux_choisi - 0.30, taux_choisi, taux_choisi + 0.30]
        duree_mois = duree_choisie * 12

        for taux in taux_list:
            taux_mensuel = taux / 100 / 12
            montant_emprunte = 0
            step = 1000
            montant_test = 100000

            while True:
                mensualite_emprunt = montant_test * ((taux_mensuel * (1 + taux_mensuel) ** duree_mois) /
                                                     ((1 + taux_mensuel) ** duree_mois - 1))
                assurance_mensuelle = montant_test * taux_assurance
                mensualite_totale = mensualite_emprunt + assurance_mensuelle
                if mensualite_totale > mensualite_max:
                    break
                montant_emprunte = montant_test
                montant_test += step

            # Affichage
            st.markdown(f"""
                #### 🔍 Résultat pour un taux de {taux:.2f}% :
                - 💰 Montant empruntable : **{montant_emprunte:,.2f} €**
                - 📉 Mensualité sans assurance : **{mensualite_emprunt:,.2f} €**
                - 🛡️ Mensualité avec assurance : **{mensualite_totale:,.2f} €**
            """)
