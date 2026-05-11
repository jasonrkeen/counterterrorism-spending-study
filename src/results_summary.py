import pandas as pd

from src.config import OUTPUT_DIR


def format_p_value(p_value: float) -> str:
    """
    Format p-values for readable reporting.
    """
    if p_value < 0.001:
        return f"{p_value:.3e}"
    return f"{p_value:.4f}"


def create_results_summary():
    """
    Create a plain-English results summary for the research paper.

    This version reads the key regression coefficients directly from
    outputs/key_regression_coefficients.csv, which is created by analysis.py.
    """

    coefficient_path = OUTPUT_DIR / "key_regression_coefficients.csv"
    summary_path = OUTPUT_DIR / "results_summary.md"

    if not coefficient_path.exists():
        raise FileNotFoundError(
            "Missing outputs/key_regression_coefficients.csv. "
            "Run python -m src.analysis first."
        )

    results_df = pd.read_csv(coefficient_path)

    required_columns = [
        "model",
        "outcome",
        "coefficient",
        "standard_error",
        "p_value",
        "statistically_significant",
    ]

    missing_columns = [
        column for column in required_columns if column not in results_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "The coefficient table is missing these columns: "
            f"{missing_columns}. Run python -m src.analysis again."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Results Summary\n\n")

        f.write("## Research Question\n\n")
        f.write(
            "This study examines whether higher military/security spending is "
            "associated with later changes in terrorist attack frequency and "
            "terrorism-related deaths. The analysis uses a country-year panel dataset "
            "covering 2001–2020.\n\n"
        )

        if "n_observations" in results_df.columns:
            n_obs = int(results_df["n_observations"].max())
            f.write(f"The final model dataset includes {n_obs:,} country-year observations.\n\n")

        f.write("## Key Regression Findings\n\n")
        f.write(
            "| Model | Outcome | Coefficient | Standard Error | P-value | Significant? |\n"
        )
        f.write("|---|---|---:|---:|---:|---|\n")

        for _, row in results_df.iterrows():
            significant = "Yes" if row["statistically_significant"] else "No"
            f.write(
                f"| {row['model']} | {row['outcome']} | "
                f"{row['coefficient']:.4f} | "
                f"{row['standard_error']:.4f} | "
                f"{format_p_value(row['p_value'])} | "
                f"{significant} |\n"
            )

        f.write("\n## Interpretation\n\n")
        f.write(
            "The year fixed effects models show a positive and statistically significant "
            "relationship between lagged military spending and both terrorist attacks and "
            "terrorism deaths. At first glance, this suggests that countries with higher "
            "prior-year military spending tend to experience more terrorism.\n\n"
        )

        f.write(
            "However, this relationship changes once country fixed effects are added. "
            "The country and year fixed effects models compare each country more closely "
            "against itself over time rather than mainly comparing high-risk countries to "
            "low-risk countries. In these stronger models, lagged military spending is no "
            "longer statistically significant for either terrorist attacks or terrorism deaths.\n\n"
        )

        f.write("## Main Finding\n\n")
        f.write(
            "The results do not provide evidence that higher military spending reduces "
            "terrorist attacks or terrorism deaths. Instead, the initial positive association "
            "appears to be driven by differences between countries. Countries facing greater "
            "terrorism risk also tend to spend more on defense and security, but increases "
            "in a country's own military spending are not clearly associated with later "
            "reductions in terrorist activity.\n\n"
        )

        f.write("## Suggested Paper Wording\n\n")
        f.write(
            "The regression results suggest that the relationship between military spending "
            "and terrorism outcomes is sensitive to model specification. In models with only "
            "year fixed effects, lagged military spending is positively and significantly "
            "associated with both terrorist attacks and terrorism deaths. However, after "
            "adding country fixed effects, the coefficient on lagged military spending becomes "
            "small and statistically insignificant. This indicates that the basic positive "
            "association likely reflects cross-country differences in terrorism risk rather "
            "than a within-country effect of spending over time. Therefore, the findings do "
            "not support the claim that higher military spending independently reduces "
            "terrorist activity.\n\n"
        )

        f.write("## Limitation\n\n")
        f.write(
            "Military expenditure is an imperfect proxy for counterterrorism spending. "
            "It includes broad defense spending and does not isolate spending specifically "
            "directed toward terrorism prevention, intelligence, law enforcement, border "
            "security, homeland security, sanctions enforcement, foreign assistance, or "
            "civilian capacity-building. Therefore, the results should be interpreted as "
            "evidence about military spending and terrorism outcomes, not as a direct test "
            "of all counterterrorism spending.\n\n"
        )

        f.write(
            "Recent counterterrorism policy sources reinforce this limitation. The State "
            "Department Bureau of Counterterrorism describes counterterrorism as involving "
            "diplomacy, partner capacity-building, border and aviation security, sanctions, "
            "countering violent extremism, and multilateral cooperation. Brown University's "
            "Costs of War project also documents that U.S. counterterrorism activity includes "
            "training, assistance, combat operations, and air or drone strikes across many "
            "countries. These sources show why aggregate military expenditure should be treated "
            "as a broad proxy rather than a precise counterterrorism spending measure.\n\n"
        )

        f.write("## Future Research\n\n")
        f.write(
            "Future research could improve on this study by using more detailed "
            "counterterrorism-specific spending measures. A narrower dataset could separate "
            "military spending, homeland security spending, foreign assistance, border security "
            "programs, intelligence-related spending, counterterrorism training, sanctions "
            "enforcement, and civilian capacity-building. This would allow researchers to test "
            "which types of counterterrorism spending are most closely associated with later "
            "changes in terrorist attacks and terrorism-related deaths.\n"
        )

    print(f"Saved written results summary to {summary_path}")


if __name__ == "__main__":
    create_results_summary()