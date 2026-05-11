import pandas as pd

from src.config import GTD_FILE, PROCESSED_DIR, START_YEAR, END_YEAR


GTD_COLUMNS_NEEDED = [
    "eventid",
    "iyear",
    "country_txt",
    "nkill",
    "nwound",
    "success",
    "suicide",
]


def load_gtd() -> pd.DataFrame:
    """
    Load only the needed columns from the Global Terrorism Database Excel file.
    """
    if not GTD_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {GTD_FILE}. "
            "Download the full GTD Excel file and rename it to globalterrorismdb.xlsx."
        )

    print(f"Loading GTD file from {GTD_FILE}...")

    df = pd.read_excel(
        GTD_FILE,
        usecols=GTD_COLUMNS_NEEDED,
    )

    print(f"Loaded GTD dataset with {len(df):,} rows.")

    return df


def build_gtd_country_year() -> pd.DataFrame:
    """
    Convert GTD event-level data into country-year terrorism indicators.
    """
    df = load_gtd()

    df = df[(df["iyear"] >= START_YEAR) & (df["iyear"] <= END_YEAR)].copy()

    df = df.dropna(subset=["country_txt", "iyear"])

    df["nkill"] = df["nkill"].fillna(0)
    df["nwound"] = df["nwound"].fillna(0)
    df["success"] = df["success"].fillna(0)
    df["suicide"] = df["suicide"].fillna(0)

    country_year = (
        df.groupby(["country_txt", "iyear"])
        .agg(
            attacks=("eventid", "count"),
            deaths=("nkill", "sum"),
            wounded=("nwound", "sum"),
            successful_attacks=("success", "sum"),
            suicide_attacks=("suicide", "sum"),
        )
        .reset_index()
    )

    country_year = country_year.rename(
        columns={
            "country_txt": "country",
            "iyear": "year",
        }
    )

    country_year["casualties"] = country_year["deaths"] + country_year["wounded"]

    country_year["fatalities_per_attack"] = (
        country_year["deaths"] / country_year["attacks"]
    )

    country_year = country_year.sort_values(["country", "year"])

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / "gtd_country_year.csv"
    country_year.to_csv(output_path, index=False)

    print(f"Saved GTD country-year data to {output_path}")
    print(country_year.head())

    return country_year


if __name__ == "__main__":
    build_gtd_country_year()