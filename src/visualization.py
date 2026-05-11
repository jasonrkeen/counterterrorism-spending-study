import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.config import PANEL_FILE, CHART_DIR


def save_global_attack_trend(df: pd.DataFrame):
    trend = (
        df.groupby("year")
        .agg(attacks=("attacks", "sum"))
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.plot(trend["year"], trend["attacks"], marker="o")
    plt.title("Global Terrorist Attacks by Year, 2001–2020")
    plt.xlabel("Year")
    plt.ylabel("Number of Attacks")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "global_attacks_by_year.png", dpi=300)
    plt.close()


def save_global_death_trend(df: pd.DataFrame):
    trend = (
        df.groupby("year")
        .agg(deaths=("deaths", "sum"))
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.plot(trend["year"], trend["deaths"], marker="o")
    plt.title("Global Terrorism Deaths by Year, 2001–2020")
    plt.xlabel("Year")
    plt.ylabel("Deaths")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "global_deaths_by_year.png", dpi=300)
    plt.close()


def save_average_attack_trend(df: pd.DataFrame):
    trend = (
        df.groupby("year")
        .agg(avg_attacks=("attacks", "mean"))
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.plot(trend["year"], trend["avg_attacks"], marker="o")
    plt.title("Average Terrorist Attacks per Country-Year")
    plt.xlabel("Year")
    plt.ylabel("Average Attacks")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "average_attacks_by_year.png", dpi=300)
    plt.close()


def save_average_death_trend(df: pd.DataFrame):
    trend = (
        df.groupby("year")
        .agg(avg_deaths=("deaths", "mean"))
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.plot(trend["year"], trend["avg_deaths"], marker="o")
    plt.title("Average Terrorism Deaths per Country-Year")
    plt.xlabel("Year")
    plt.ylabel("Average Deaths")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "average_deaths_by_year.png", dpi=300)
    plt.close()


def save_spending_vs_attacks(df: pd.DataFrame):
    plot_df = df.dropna(subset=["military_spending_billions", "attacks"]).copy()

    plt.figure(figsize=(10, 6))
    plt.scatter(
        plot_df["military_spending_billions"],
        plot_df["attacks"],
        alpha=0.5,
    )
    plt.title("Military Spending vs. Terrorist Attacks")
    plt.xlabel("Military Spending, Current US$ Billions")
    plt.ylabel("Terrorist Attacks")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "spending_vs_attacks.png", dpi=300)
    plt.close()


def save_log_spending_vs_log_attacks(df: pd.DataFrame):
    plot_df = df.dropna(
        subset=["military_spending_billions", "attacks"]
    ).copy()

    plot_df = plot_df[plot_df["military_spending_billions"] > 0]

    plot_df["log_spending_billions"] = np.log1p(plot_df["military_spending_billions"])
    plot_df["log_attacks_plot"] = np.log1p(plot_df["attacks"])

    plt.figure(figsize=(10, 6))
    plt.scatter(
        plot_df["log_spending_billions"],
        plot_df["log_attacks_plot"],
        alpha=0.5,
    )
    plt.title("Log Military Spending vs. Log Terrorist Attacks")
    plt.xlabel("Log Military Spending, Current US$ Billions")
    plt.ylabel("Log Terrorist Attacks")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "log_spending_vs_log_attacks.png", dpi=300)
    plt.close()


def save_log_spending_vs_log_deaths(df: pd.DataFrame):
    plot_df = df.dropna(
        subset=["military_spending_billions", "deaths"]
    ).copy()

    plot_df = plot_df[plot_df["military_spending_billions"] > 0]

    plot_df["log_spending_billions"] = np.log1p(plot_df["military_spending_billions"])
    plot_df["log_deaths_plot"] = np.log1p(plot_df["deaths"])

    plt.figure(figsize=(10, 6))
    plt.scatter(
        plot_df["log_spending_billions"],
        plot_df["log_deaths_plot"],
        alpha=0.5,
    )
    plt.title("Log Military Spending vs. Log Terrorism Deaths")
    plt.xlabel("Log Military Spending, Current US$ Billions")
    plt.ylabel("Log Terrorism Deaths")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "log_spending_vs_log_deaths.png", dpi=300)
    plt.close()


def save_log_lagged_spending_vs_log_attacks(df: pd.DataFrame):
    plot_df = df.dropna(
        subset=["log_military_spending_lag1", "log_attacks"]
    ).copy()

    plt.figure(figsize=(10, 6))
    plt.scatter(
        plot_df["log_military_spending_lag1"],
        plot_df["log_attacks"],
        alpha=0.5,
    )
    plt.title("Lagged Log Military Spending vs. Log Terrorist Attacks")
    plt.xlabel("Lagged Log Military Spending (t-1)")
    plt.ylabel("Log Terrorist Attacks")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "lagged_log_spending_vs_log_attacks.png", dpi=300)
    plt.close()


def save_log_lagged_spending_vs_log_deaths(df: pd.DataFrame):
    plot_df = df.dropna(
        subset=["log_military_spending_lag1", "log_deaths"]
    ).copy()

    plt.figure(figsize=(10, 6))
    plt.scatter(
        plot_df["log_military_spending_lag1"],
        plot_df["log_deaths"],
        alpha=0.5,
    )
    plt.title("Lagged Log Military Spending vs. Log Terrorism Deaths")
    plt.xlabel("Lagged Log Military Spending (t-1)")
    plt.ylabel("Log Terrorism Deaths")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "lagged_log_spending_vs_log_deaths.png", dpi=300)
    plt.close()


def save_top_countries_by_attacks(df: pd.DataFrame, n: int = 10):
    top = (
        df.groupby("country")
        .agg(attacks=("attacks", "sum"))
        .sort_values("attacks", ascending=False)
        .head(n)
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.barh(top["country"], top["attacks"])
    plt.gca().invert_yaxis()
    plt.title(f"Top {n} Countries by Terrorist Attacks, 2001–2020")
    plt.xlabel("Total Attacks")
    plt.ylabel("Country")
    plt.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "top_countries_by_attacks.png", dpi=300)
    plt.close()


def save_top_countries_by_deaths(df: pd.DataFrame, n: int = 10):
    top = (
        df.groupby("country")
        .agg(deaths=("deaths", "sum"))
        .sort_values("deaths", ascending=False)
        .head(n)
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.barh(top["country"], top["deaths"])
    plt.gca().invert_yaxis()
    plt.title(f"Top {n} Countries by Terrorism Deaths, 2001–2020")
    plt.xlabel("Total Deaths")
    plt.ylabel("Country")
    plt.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "top_countries_by_deaths.png", dpi=300)
    plt.close()


def save_spending_trend_for_top_countries(df: pd.DataFrame, n: int = 5):
    top_countries = (
        df.groupby("country")
        .agg(attacks=("attacks", "sum"))
        .sort_values("attacks", ascending=False)
        .head(n)
        .index
        .tolist()
    )

    plot_df = df[df["country"].isin(top_countries)].copy()
    plot_df = plot_df.dropna(subset=["military_spending_billions"])

    plt.figure(figsize=(11, 7))

    for country in top_countries:
        country_df = plot_df[plot_df["country"] == country].sort_values("year")
        plt.plot(
            country_df["year"],
            country_df["military_spending_billions"],
            marker="o",
            label=country,
        )

    plt.title(f"Military Spending Trends for Top {n} Terrorism-Affected Countries")
    plt.xlabel("Year")
    plt.ylabel("Military Spending, Current US$ Billions")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "spending_trend_top_countries.png", dpi=300)
    plt.close()


def save_log_spending_trend_for_top_countries(df: pd.DataFrame, n: int = 5):
    top_countries = (
        df.groupby("country")
        .agg(attacks=("attacks", "sum"))
        .sort_values("attacks", ascending=False)
        .head(n)
        .index
        .tolist()
    )

    plot_df = df[df["country"].isin(top_countries)].copy()
    plot_df = plot_df.dropna(subset=["military_spending_billions"])

    plt.figure(figsize=(11, 7))

    for country in top_countries:
        country_df = plot_df[plot_df["country"] == country].sort_values("year").copy()
        country_df["log_spending_billions"] = np.log1p(country_df["military_spending_billions"])

        plt.plot(
            country_df["year"],
            country_df["log_spending_billions"],
            marker="o",
            label=country,
        )

    plt.title(f"Log Military Spending Trends for Top {n} Terrorism-Affected Countries")
    plt.xlabel("Year")
    plt.ylabel("Log Military Spending, Current US$ Billions")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "log_spending_trend_top_countries.png", dpi=300)
    plt.close()


def save_chart_data_tables(df: pd.DataFrame):
    """
    Save the data used in selected charts so the numbers can be cited in the paper.
    """
    global_trend = (
        df.groupby("year")
        .agg(
            total_attacks=("attacks", "sum"),
            total_deaths=("deaths", "sum"),
            total_wounded=("wounded", "sum"),
            avg_attacks=("attacks", "mean"),
            avg_deaths=("deaths", "mean"),
        )
        .reset_index()
    )

    top_countries = (
        df.groupby("country")
        .agg(
            total_attacks=("attacks", "sum"),
            total_deaths=("deaths", "sum"),
            total_wounded=("wounded", "sum"),
            avg_military_spending_billions=("military_spending_billions", "mean"),
        )
        .sort_values("total_attacks", ascending=False)
        .reset_index()
    )

    global_trend.to_csv(CHART_DIR / "chart_data_global_trends.csv", index=False)
    top_countries.to_csv(CHART_DIR / "chart_data_top_countries.csv", index=False)


def save_correlation_matrix(df: pd.DataFrame):
    corr_df = df[
        [
            "attacks",
            "deaths",
            "wounded",
            "military_spending_billions",
            "military_spending_pct_gdp",
            "military_spending_lag1",
            "log_attacks",
            "log_deaths",
            "log_military_spending_lag1",
            "log_gdp",
            "log_population",
        ]
    ].copy()

    correlation_matrix = corr_df.corr(numeric_only=True)
    correlation_matrix.to_csv(CHART_DIR / "correlation_matrix.csv")


def build_charts():
    if not PANEL_FILE.exists():
        raise FileNotFoundError(
            "Missing terrorism_spending_panel.csv. Run merge_data.py first."
        )

    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(PANEL_FILE)

    save_global_attack_trend(df)
    save_global_death_trend(df)
    save_average_attack_trend(df)
    save_average_death_trend(df)

    save_spending_vs_attacks(df)
    save_log_spending_vs_log_attacks(df)
    save_log_spending_vs_log_deaths(df)
    save_log_lagged_spending_vs_log_attacks(df)
    save_log_lagged_spending_vs_log_deaths(df)

    save_top_countries_by_attacks(df)
    save_top_countries_by_deaths(df)

    save_spending_trend_for_top_countries(df)
    save_log_spending_trend_for_top_countries(df)

    save_chart_data_tables(df)
    save_correlation_matrix(df)

    print(f"Saved charts and chart data tables to {CHART_DIR}")


if __name__ == "__main__":
    build_charts()