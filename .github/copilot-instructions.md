# Copilot instructions: Counterterrorism Spending and Terrorist Attack Severity

## Purpose
Quantitative Python study of military spending and terrorist attack severity using GTD event data, World Bank/SIPRI indicators, visualizations, and fixed-effects regression models.

## Tech stack
- Python; dependencies in `requirements.txt`
- Key libraries: `pandas`, `numpy`, `requests`, `matplotlib`, `seaborn`, `statsmodels`, `scikit-learn`, `openpyxl`, `pycountry`

## Folder structure
- `data/` (3 files)
- `outputs/` (21 files)
- `src/` (8 files)
- `README.md`
- `counterterrorism_spending_final_report.pdf`
- `main.py`
- `requirements.txt`

## Setup, run, test
Commands documented in README.md (referenced files exist):
```bash
pip install -r requirements.txt
python main.py
```
- No automated tests exist yet; if adding them, use pytest under `tests/`.

## Conventions observed
- Functions use type hints; keep annotating new code.
- Config lives in: `src/config.py`; avoid hardcoding parameters elsewhere.
- Raw data (`data/raw/`) is gitignored; download/fetch it via the pipeline, do not commit it.
- Public data sources referenced: World Bank, GTD, SIPRI.
- Write paths relative to the repo root (no absolute local paths).

## Output artifacts
- Generated outputs go to: `outputs/charts/`
- A PDF report is produced; keep it in sync with model changes.
- Charts are generated with matplotlib.

## Guardrails
- Never commit secrets, API keys, tokens, or `.env` files.
- Do not commit large raw datasets or binaries; keep data fetched or documented with its source.
- Keep analysis source-backed: cite data sources and assumptions; label scenario/forecast outputs as model estimates, not facts.
- Preserve reproducibility: no unseeded randomness, no hidden manual steps.
