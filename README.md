# 💼 OptiCrédit – Simulateur de financement immobilier

Bienvenue sur **OptiCrédit**, un outil professionnel développé avec [Streamlit](https://streamlit.io) pour accompagner les particuliers et conseillers en gestion de patrimoine dans la simulation de projets immobiliers.

---

## 🧮 Fonctions disponibles

L’application propose plusieurs **calculettes interactives** :

- **Capacité d’emprunt (sur 3 durées fixes)** : calculez le montant qu’un client peut emprunter en fonction de ses revenus et charges.
- **Capacité d’emprunt avec variation de taux** : explorez l’impact d’un taux plus haut ou plus bas sur le capital empruntable.
- **Calcul de mensualité** : obtenez la mensualité à partir d’un montant, d’une durée et d’un taux.
- **Calcul du capital empruntable à partir d’une mensualité**.
- **Simulation de rachat de prêt** : avec intégration du taux, de la durée restante, et du différentiel.

---

## 🎨 Design et charte

- Couleurs : **rouge #C32026**, **gris clair #F4F4F4**, **texte noir**
- Interface sobre et élégante, fidèle à la charte de [Talan Patrimoine](https://talan-patrimoine.fr)
- Responsive et lisible même sur tablette

---

## 🛠 Technologies utilisées

- [Streamlit](https://streamlit.io) — interface web
- `pandas`, `numpy` — calculs et tableaux
- `datetime`, `dateutil` — gestion des âges et échéances
- `reportlab` (à venir) — génération de PDF

---

## 🚀 Déploiement

1. Cloner ce dépôt :
   ```bash
   git clone https://github.com/votre-organisation/opticredit-app.git
