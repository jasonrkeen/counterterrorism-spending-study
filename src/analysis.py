import pandas as pd
import statsmodels.formula.api as smf

from src.config import PANEL_FILE, OUTPUT_DIR


def write_model_summary(file, title: str, model):
    """
    Write a regression model summary safely.
    If statsmodels cannot generate the full summary table, write key results instead.
    """
    file.write(title + "\n")
    file.write("-" * 80 + "\n")

    try:
        file.write(model.summary().as_text())
    except Exception as error:
        file.write("Full statsmodels summary could not be generated.\n")
        file.write(f"Reason: {error}\n\n")
        file.write("Key coefficient results:\n")
        file.write(str(model.params))
        file.write("\n\nStandard errors:\n")
        file.write(str(model.bse))
        file.write("\n\nP-values:\n")
        file.write(str(model.pvalues))

    file.write("\n\n")


def extract_key_result(model, model_name: str, outcome: str) -> dict:
    """
    Extract the lagged military spending coefficient, standard error, and p-value.
    """
    variable = "log_military_spending_lag1"

    return {
        "model": model_name,
        "outcome": outcome,
        "variable": variable,
        "coefficient": model.params.get(variable),
        "standard_error": model.bse.get(variable),
        "p_value": model.pvalues.get(variable),
        "statistically_significant": model.pvalues.get(variable) < 0.05,
        "r_squared": model.rsquared,
        "n_observations": int(model.nobs),
    }


def run_analysis():
    if not PANEL_FILE.exists():
        raise FileNotFoundError(
            "Missing terrorism_spending_panel.csv. Run merge_data.py first."
        )

    df = pd.read_csv(PANEL_FILE)

    model_df = df.dropna(
        subset=[
            "attacks",
            "deaths",
            "log_attacks",
            "log_deaths",
            "log_military_spending_lag1",
            "log_gdp",
            "log_population",
            "country",
            "year",
        ]
    ).copy()

    print("\nDataset shape used in models:")
    print(model_df.shape)

    print("\nSummary statistics:")
    summary = model_df[
        [
            "attacks",
            "deaths",
            "wounded",
            "military_spending_billions",
            "military_spending_pct_gdp",
            "gdp_billions",
            "population",
        ]
    ].describe()

    print(summary)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_DIR / "summary_statistics.csv")

    # ------------------------------------------------------------------
    # MODEL 1: Basic models with year fixed effects only
    # ------------------------------------------------------------------
    model_attacks_basic = smf.ols(
        formula=(
            "log_attacks ~ log_military_spending_lag1 "
            "+ log_gdp + log_population + C(year)"
        ),
        data=model_df,
    ).fit(cov_type="HC3")

    model_deaths_basic = smf.ols(
        formula=(
            "log_deaths ~ log_military_spending_lag1 "
            "+ log_gdp + log_population + C(year)"
        ),
        data=model_df,
    ).fit(cov_type="HC3")

    # ------------------------------------------------------------------
    # MODEL 2: Stronger panel models with country and year fixed effects
    # Clustered standard errors by country are better for panel data.
    # ------------------------------------------------------------------
    model_attacks_country_fe = smf.ols(
        formula=(
            "log_attacks ~ log_military_spending_lag1 "
            "+ log_gdp + log_population + C(year) + C(country)"
        ),
        data=model_df,
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": model_df["country"]},
    )

    model_deaths_country_fe = smf.ols(
        formula=(
            "log_deaths ~ log_military_spending_lag1 "
            "+ log_gdp + log_population + C(year) + C(country)"
        ),
        data=model_df,
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": model_df["country"]},
    )

    results_path = OUTPUT_DIR / "regression_results.txt"

    with open(results_path, "w", encoding="utf-8") as f:
        f.write("COUNTERTERRORISM SPENDING AND TERRORISM OUTCOMES\n")
        f.write("=" * 80)
        f.write("\n\n")

        write_model_summary(
            f,
            "MODEL 1A: Log terrorist attacks — year fixed effects only",
            model_attacks_basic,
        )

        write_model_summary(
            f,
            "MODEL 1B: Log terrorism deaths — year fixed effects only",
            model_deaths_basic,
        )

        write_model_summary(
            f,
            "MODEL 2A: Log terrorist attacks — country and year fixed effects",
            model_attacks_country_fe,
        )

        write_model_summary(
            f,
            "MODEL 2B: Log terrorism deaths — country and year fixed effects",
            model_deaths_country_fe,
        )

        f.write("INTERPRETATION NOTES\n")
        f.write("-" * 80)
        f.write("\n")
        f.write(
            "The year fixed effects models compare countries to each other while "
            "controlling for global year shocks. The country and year fixed effects "
            "models are stronger because they compare each country more closely "
            "against itself over time. This helps control for time-invariant country "
            "characteristics such as geography, long-run institutional differences, "
            "and persistent regional security conditions.\n\n"
        )
        f.write(
            "The coefficient on lagged military spending should be interpreted as an "
            "association, not as a causal effect. A positive coefficient may reflect "
            "threat-driven spending, where countries experiencing more terrorism risk "
            "increase military and security expenditure in response.\n\n"
        )
        f.write(
            "Because terrorist attacks and deaths are count-based outcomes with many "
            "small values and a few very large values, later versions of this project "
            "may also use Poisson or negative binomial models as robustness checks.\n"
        )

    key_results = [
        extract_key_result(
            model_attacks_basic,
            "Model 1A — Year FE attacks model",
            "Log terrorist attacks",
        ),
        extract_key_result(
            model_deaths_basic,
            "Model 1B — Year FE deaths model",
            "Log terrorism deaths",
        ),
        extract_key_result(
            model_attacks_country_fe,
            "Model 2A — Country and Year FE attacks model",
            "Log terrorist attacks",
        ),
        extract_key_result(
            model_deaths_country_fe,
            "Model 2B — Country and Year FE deaths model",
            "Log terrorism deaths",
        ),
    ]

    key_results_df = pd.DataFrame(key_results)
    key_results_path = OUTPUT_DIR / "key_regression_coefficients.csv"
    key_results_df.to_csv(key_results_path, index=False)

    print(f"\nSaved regression results to {results_path}")
    print(f"Saved key coefficient table to {key_results_path}")

    print("\nKey coefficients for lagged military spending:")
    print("-" * 60)

    for result in key_results:
        print(result["model"])
        print("Coefficient:", result["coefficient"])
        print("Standard error:", result["standard_error"])
        print("P-value:", result["p_value"])
        print("Significant:", result["statistically_significant"])
        print()


if __name__ == "__main__":
    run_analysis()