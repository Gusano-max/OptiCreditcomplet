from datetime import datetime

def calcul_mensualite(capital, taux_annuel, duree_mois):
    taux_mensuel = taux_annuel / 100 / 12
    if taux_mensuel == 0:
        return capital / duree_mois
    return capital * taux_mensuel / (1 - (1 + taux_mensuel) ** -duree_mois)

def calcul_assurance_mensuelle(capital, taux_assurance):
    return capital * (taux_assurance / 100) / 12

def get_taux_assurance(date_naissance: datetime.date) -> float:
    naissance_dt = datetime.combine(date_naissance, datetime.min.time())
    age = (datetime.today() - naissance_dt).days // 365
    if age < 30:
        return 0.15
    elif age <= 50:
        return 0.30
    else:
        return 0.50

