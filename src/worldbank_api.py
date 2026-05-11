import requests
import pandas as pd

from src.config import START_YEAR, END_YEAR, PROCESSED_DIR


INDICATORS = {
    "gdp_current_usd": "NY.GDP.MKTP.CD",
    "population": "SP.POP.TOTL",
    "military_spending_current_usd": "MS.MIL.XPND.CD",
    "military_spending_pct_gdp": "MS.MIL.XPND.GD.ZS",
}


def fetch_worldbank_indicator(indicator_code: str, indicator_name: str) -> pd.DataFrame:
    """
    Fetch country-year data from the World Bank API.

    This function handles pagination so the full dataset is retrieved even if
    the World Bank API splits the response across multiple pages.
    """
    rows = []
    page = 1
    per_page = 20000

    while True:
        url = (
            f"https://api.worldbank.org/v2/country/all/indicator/{indicator_code}"
            f"?format=json&per_page={per_page}&page={page}"
        )

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list) or len(data) < 2:
            raise ValueError(f"Unexpected World Bank API response for {indicator_code}")

        metadata = data[0]
        records = data[1]

        if not records:
            break

        for item in records:
            country = item.get("country", {}).get("value")
            country_code = item.get("countryiso3code")
            year = item.get("date")
            value = item.get("value")

            if not country_code or not year:
                continue

            try:
                year = int(year)
            except ValueError:
                continue

            if START_YEAR <= year <= END_YEAR:
                rows.append(
                    {
                        "country": country,
                        "iso3": country_code,
                        "year": year,
                        indicator_name: value,
                    }
                )

        total_pages = int(metadata.get("pages", 1))

        if page >= total_pages:
            break

        page += 1

    df = pd.DataFrame(rows)

    print(
        f"Fetched {len(df):,} rows for {indicator_name} "
        f"({indicator_code}), {START_YEAR}-{END_YEAR}."
    )

    return df


def build_worldbank_dataset() -> pd.DataFrame:
    """
    Build one World Bank dataset with GDP, population, and military spending variables.
    """
    frames = []

    for indicator_name, indicator_code in INDICATORS.items():
        print(f"Fetching {indicator_name}...")
        df = fetch_worldbank_indicator(indicator_code, indicator_name)
        frames.append(df)

    merged = frames[0]

    for frame in frames[1:]:
        merged = merged.merge(
            frame,
            on=["country", "iso3", "year"],
            how="outer",
        )

    merged = merged.sort_values(["iso3", "year"])

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / "worldbank_data.csv"
    merged.to_csv(output_path, index=False)

    print(f"Saved World Bank data to {output_path}")
    print(merged.head())

    return merged


if __name__ == "__main__":
    build_worldbank_dataset()