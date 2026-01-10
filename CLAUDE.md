# OptiCrédit V2 - Simulateur de Crédit Immobilier

## 🎯 Objectif
Refonte complète de OptiCrédit avec interface moderne Streamlit.

## 📋 Fonctionnalités
- Simulation crédit immobilier (mensualités, TAEG, coût total)
- Capacité d'emprunt
- Comparaison de scénarios
- Export PDF des résultats
- Interface moderne et intuitive

## 🏗️ Architecture
```
opticredit-v2/
├── app.py                # Application Streamlit principale
├── src/
│   ├── calculator.py     # Logique de calcul
│   ├── data_handler.py   # Gestion données
│   └── export.py         # Export PDF
├── utils/
│   └── helpers.py        # Fonctions utilitaires
├── assets/
│   └── logo.png          # Logo Talan Patrimoine
├── requirements.txt
└── README.md
```

## 🛠️ Stack Technique
- Python 3.14+
- Streamlit (interface)
- Pandas (données)
- FPDF ou ReportLab (export PDF)
- Plotly (graphiques)

## 📝 Conventions de Code
- PEP 8 (style Python)
- Type hints partout
- Docstrings sur toutes les fonctions
- Tests pour les calculs
- Messages en français (interface)

## ❌ Interdictions
- Pas de sudo
- Pas d'accès fichiers système
- Demander permission avant packages

## 🧪 Tests de Validation
1. Calcul mensualité avec taux fixe
2. Calcul capacité d'emprunt
3. Export PDF généré
4. Interface responsive
5. Graphiques affichés

## 🎨 Design
- Couleurs Talan Patrimoine
- Design moderne et épuré
- Mobile-friendly
