import numpy as np
import pandas as pd

from src.config import PROCESSED_DIR, PANEL_FILE


COUNTRY_NAME_MAP = {
    "Bahamas": "Bahamas, The",
    "Bolivia": "Bolivia",
    "Brunei": "Brunei Darussalam",
    "Congo (Brazzaville)": "Congo, Rep.",
    "Democratic Republic of the Congo": "Congo, Dem. Rep.",
    "Egypt": "Egypt, Arab Rep.",
    "Gambia": "Gambia, The",
    "Hong Kong": "Hong Kong SAR, China",
    "Iran": "Iran, Islamic Rep.",
    "Ivory Coast": "Cote d'Ivoire",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Laos": "Lao PDR",
    "Macedonia": "North Macedonia",
    "Russia": "Russian Federation",
    "Slovak Republic": "Slovakia",
    "South Korea": "Korea, Rep.",
    "Syria": "Syrian Arab Republic",
    "Turkey": "Turkiye",
    "United States": "United States",
    "Venezuela": "Venezuela, RB",
    "Vietnam": "Viet Nam",
    "West Bank and Gaza Strip": "West Bank and Gaza",
    "Yemen": "Yemen, Rep.",
}


def clean_gtd_country_names(gtd: pd.DataFrame) -> pd.DataFrame:
    """
    Clean GTD country names so they better match World Bank country names.
    """
    gtd = gtd.copy()
    gtd["country_original"] = gtd["country"]
    gtd["country"] = gtd["country"].replace(COUNTRY_NAME_MAP)
    return gtd


def report_merge_quality(panel: pd.DataFrame) -> None:
    """
    Print basic diagnostics showing how well GTD matched with World Bank data.
    """
    total_rows = len(panel)

    missing_spending = panel["military_spending_current_usd"].isna().sum()
    missing_gdp = panel["gdp_current_usd"].isna().sum()
    missing_population = panel["population"].isna().sum()

    print("\nMerge quality report:")
    print("-" * 60)
    print(f"Total panel rows: {total_rows:,}")
    print(f"Rows missing military spending: {missing_spending:,}")
    print(f"Rows missing GDP: {missing_gdp:,}")
    print(f"Rows missing population: {missing_population:,}")

    unmatched = (
        panel[panel["gdp_current_usd"].isna()]
        .groupby("country_original", dropna=False)
        .size()
        .sort_values(ascending=False)
        .head(25)
    )

    if not unmatched.empty:
        print("\nTop unmatched GTD country names:")
        print(unmatched)


def merge_panel_data() -> pd.DataFrame:
    gtd_path = PROCESSED_DIR / "gtd_country_year.csv"
    wb_path = PROCESSED_DIR / "worldbank_data.csv"

    if not gtd_path.exists():
        raise FileNotFoundError(
            "Missing gtd_country_year.csv. Run gtd_processing.py first."
        )

    if not wb_path.exists():
        raise FileNotFoundError(
            "Missing worldbank_data.csv. Run worldbank_api.py first."
        )

    gtd = pd.read_csv(gtd_path)
    wb = pd.read_csv(wb_path)

    gtd = clean_gtd_country_names(gtd)

    panel = gtd.merge(
        wb,
        on=["country", "year"],
        how="left",
    )

    panel = panel.sort_values(["country", "year"])

    # Spending and GDP transformations
    panel["military_spending_billions"] = (
        panel["military_spending_current_usd"] / 1_000_000_000
    )

    panel["gdp_billions"] = panel["gdp_current_usd"] / 1_000_000_000

    panel["military_spending_per_capita"] = (
        panel["military_spending_current_usd"] / panel["population"]
    )

    # Lagged variables to reduce same-year reverse-causality concerns.
    panel["military_spending_lag1"] = (
        panel.groupby("country")["military_spending_current_usd"].shift(1)
    )

    panel["military_spending_pct_gdp_lag1"] = (
        panel.groupby("country")["military_spending_pct_gdp"].shift(1)
    )

    # Log transformations
    panel["log_attacks"] = np.log1p(panel["attacks"])
    panel["log_deaths"] = np.log1p(panel["deaths"])
    panel["log_wounded"] = np.log1p(panel["wounded"])
    panel["log_casualties"] = np.log1p(panel["casualties"])

    panel["log_military_spending"] = np.log1p(
        panel["military_spending_current_usd"]
    )

    panel["log_military_spending_lag1"] = np.log1p(
        panel["military_spending_lag1"]
    )

    panel["log_gdp"] = np.log1p(panel["gdp_current_usd"])
    panel["log_population"] = np.log1p(panel["population"])

    report_merge_quality(panel)

    PANEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(PANEL_FILE, index=False)

    print(f"\nSaved merged panel dataset to {PANEL_FILE}")
    print(panel.head())

    return panel


if __name__ == "__main__":
    merge_panel_data()