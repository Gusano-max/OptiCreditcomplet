import streamlit as st
from style_utils import configure_page, apply_custom_css, afficher_logo, ligne_decorative, encart_contact, titre_avec_ligne


configure_page(title="Simulation de rachat de prêt", icon="📉")
apply_custom_css()
afficher_logo()

st.markdown("<h3 style='text-align:center;'>Calculette de capacité de financement</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Calculez votre capacité d'emprunt sur 3 durées</h3>", unsafe_allow_html=True)
ligne_decorative() 


st.markdown("#### Informations personnelles et financières")
date_naissance = st.text_input("Date de naissance (JJ/MM/AAAA)", "")
revenus_salariaux = st.number_input("Revenus salariaux (€)", min_value=0.0, format="%.2f")
revenus_locatifs = st.number_input("Revenus locatifs (seront pondérés automatiquement à 70%)", min_value=0.0, format="%.2f")
mensualite_credit_en_cours = st.number_input("Mensualité de crédits en cours (€)", min_value=0.0, format="%.2f")

st.markdown("#### Taux d'intérêt annuels")
taux_annuel_15 = st.number_input("Taux d'intérêt annuel pour 15 ans (%)", min_value=0.0, format="%.2f")
taux_annuel_20 = st.number_input("Taux d'intérêt annuel pour 20 ans (%)", min_value=0.0, format="%.2f")
taux_annuel_25 = st.number_input("Taux d'intérêt annuel pour 25 ans (%)", min_value=0.0, format="%.2f")

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

        # Calcul de la mensualité maximale disponible (assurance incluse)
        mensualite_max = (revenus_salariaux + 0.7 * revenus_locatifs) * 0.35 - mensualite_credit_en_cours

        resultats = f"**Mensualité maximale (assurance incluse)** : {mensualite_max:,.2f}€\n\n"

        # Pour chaque durée, on détermine le montant empruntable
        for duree, taux_annuel in zip((15, 20, 25), (taux_annuel_15, taux_annuel_20, taux_annuel_25)):
            taux_mensuel = taux_annuel / 12 / 100
            duree_mois = duree * 12

            montant_emprunte = 0
            step = 1000
            montant_test = 100000  # point de départ

            # On augmente par pas de 1000 jusqu'à dépasser la capacité de paiement
            while True:
                mensualite_emprunt = montant_test * ((taux_mensuel * (1 + taux_mensuel) ** duree_mois) /
                                                     ((1 + taux_mensuel) ** duree_mois - 1))
                assurance_mensuelle = montant_test * taux_assurance
                mensualite_totale = mensualite_emprunt + assurance_mensuelle
                if mensualite_totale > mensualite_max:
                    break
                montant_emprunte = montant_test
                montant_test += step

            # Recalcul des mensualités à partir du montant emprunté validé
            mensualite_emprunt_final = montant_emprunte * ((taux_mensuel * (1 + taux_mensuel) ** duree_mois) /
                                                           ((1 + taux_mensuel) ** duree_mois - 1))
            assurance_mensuelle_final = montant_emprunte * taux_assurance
            mensualite_totale_final = mensualite_emprunt_final + assurance_mensuelle_final

            resultats += (
                f"**Durée : {duree} ans**\n"
                f"- Montant empruntable : {montant_emprunte:,.2f}€\n"
                f"- Mensualité sans assurance : {mensualite_emprunt_final:,.2f}€\n"
                f"- Mensualité avec assurance : {mensualite_totale_final:,.2f}€ (Max autorisé)\n\n"
            )
        
        from style_utils import afficher_resultats_markdown
        afficher_resultats_markdown(resultats)



encart_contact()
