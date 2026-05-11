from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

OUTPUT_DIR = BASE_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"

START_YEAR = 2001
END_YEAR = 2020

# Place the full GTD Excel file in data/raw and rename it to this:
GTD_FILE = RAW_DIR / "globalterrorismdb.xlsx"

PANEL_FILE = PROCESSED_DIR / "terrorism_spending_panel.csv"