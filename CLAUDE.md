# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OptiCredit is a mortgage/real estate loan simulation tool built for Talan Patrimoine. It provides interactive calculators for borrowing capacity, monthly payments, loan buyback simulation, and deferred amortization. Deployed on Streamlit Cloud at https://opti-credit-complet.streamlit.app/

## Commands

```bash
# Run the app locally
streamlit run Accueil.py

# Install dependencies
pip install -r requirements.txt
```

There are no automated tests or linting configured in this project.

## Architecture

This is a **Streamlit multi-page app**. Streamlit auto-discovers pages from the `pages/` directory and displays them in the sidebar navigation.

- **`Accueil.py`** - Entry point / home page. Streamlit uses this as the main page.
- **`pages/`** - Each file is a standalone calculator page. Files are prefixed with numbers for sidebar ordering (1_ through 6_). File names contain spaces and accented characters.
- **`utils.py`** - Core financial calculation functions: `calcul_mensualite()`, `calcul_assurance_mensuelle()`, `get_taux_assurance()`. These are pure functions with no Streamlit dependency.
- **`style_utils.py`** - All shared UI components: page config, CSS theming, logo display, decorative elements, result formatting, contact box, input validation. Every page imports and calls `configure_page()`, `apply_custom_css()`, `afficher_logo()` at the top.
- **`.streamlit/config.toml`** - Theme config (colors, font) and `fileWatcherType = "none"`.

### Page pattern

Every page follows the same structure:
1. Import from `style_utils` and `utils`
2. Call `configure_page()`, `apply_custom_css()`, `afficher_logo()`
3. Display title with `st.markdown` + `ligne_decorative()`
4. Collect inputs via `st.number_input`, `st.date_input`, etc.
5. Perform calculations and display results
6. Call `encart_contact()` at the bottom

### Key financial functions

- `calcul_mensualite(capital, taux_annuel, duree_mois)` - Monthly payment from capital, annual rate (%), and duration in months
- `calcul_assurance_mensuelle(capital, taux_assurance)` - Monthly insurance from capital and annual insurance rate (%)
- `get_taux_assurance(date_naissance)` - Returns insurance rate based on age brackets (<30: 0.15%, 30-50: 0.30%, >50: 0.50%)

## Conventions

- **Language**: All UI text, variable names, comments, and labels are in French
- **Currency formatting**: Use `format_nombre()` from `style_utils` (French format: `1 234,56 €`)
- **Branding**: Red `#C32026`, light gray `#F4F4F4`, black text. Logo is `logo.webp` at project root.
- **PDF export**: Uses `fpdf` (FPDF class) with latin-1 encoding fallback for special characters
- **Dependencies**: streamlit, numpy, pandas, python-dateutil, reportlab, fpdf
