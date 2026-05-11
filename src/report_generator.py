import pandas as pd

from src.config import OUTPUT_DIR, CHART_DIR


def format_p_value(p_value: float) -> str:
    """
    Format p-values for readable reporting.
    """
    if p_value < 0.001:
        return f"{p_value:.3e}"
    return f"{p_value:.4f}"


def load_key_regression_results() -> pd.DataFrame:
    """
    Load the key regression coefficient table created by analysis.py.
    """
    coefficient_path = OUTPUT_DIR / "key_regression_coefficients.csv"

    if not coefficient_path.exists():
        raise FileNotFoundError(
            "Missing outputs/key_regression_coefficients.csv. "
            "Run python -m src.analysis first."
        )

    return pd.read_csv(coefficient_path)


def create_final_report():
    """
    Create a polished final markdown report for the project.
    """

    report_path = OUTPUT_DIR / "final_report.md"
    regression_results = load_key_regression_results()

    chart_list = [
        "global_attacks_by_year.png",
        "global_deaths_by_year.png",
        "average_attacks_by_year.png",
        "average_deaths_by_year.png",
        "top_countries_by_attacks.png",
        "top_countries_by_deaths.png",
        "log_spending_vs_log_attacks.png",
        "log_spending_vs_log_deaths.png",
        "lagged_log_spending_vs_log_attacks.png",
        "lagged_log_spending_vs_log_deaths.png",
        "log_spending_trend_top_countries.png",
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Counterterrorism Spending and Terrorist Attack Severity\n\n")

        f.write("## Introduction\n\n")
        f.write(
            "This project examines the relationship between terrorism outcomes and "
            "military/security spending using a country-year panel dataset from 2001 "
            "to 2020. The central research question is whether higher prior-year "
            "military spending is associated with fewer terrorist attacks or fewer "
            "terrorism-related deaths.\n\n"
        )

        f.write(
            "The study uses military expenditure as a proxy for security and "
            "counterterrorism-related spending. This proxy is imperfect because military "
            "expenditure includes broad defense spending and does not isolate spending "
            "specifically directed toward counterterrorism, intelligence, policing, border "
            "security, or prevention programs. For that reason, the findings should be "
            "interpreted as evidence about the relationship between military spending "
            "and terrorism outcomes, not as a direct causal estimate of counterterrorism "
            "program effectiveness.\n\n"
        )

        f.write("## Data\n\n")
        f.write(
            "The terrorism data come from the Global Terrorism Database and are aggregated "
            "from incident-level observations into country-year totals. The main terrorism "
            "outcomes are the number of terrorist attacks, terrorism deaths, wounded victims, "
            "casualties, and fatalities per attack. Military expenditure, GDP, and population "
            "data are taken from World Bank/SIPRI indicators and merged into the country-year "
            "panel.\n\n"
        )

        if "n_observations" in regression_results.columns:
            n_obs = int(regression_results["n_observations"].max())
            f.write(
                f"The final model dataset includes {n_obs:,} country-year observations.\n\n"
            )
        else:
            f.write(
                "The final model dataset includes the country-year observations retained "
                "after merging terrorism and spending data.\n\n"
            )

        f.write("## Policy Context: Why Military Spending Is Only a Proxy\n\n")
        f.write(
            "A central challenge in this project is that counterterrorism spending is not "
            "reported as one clean, globally comparable category. Military expenditure is "
            "available across many countries and years, which makes it useful for a broad "
            "country-year study, but counterterrorism policy extends far beyond military "
            "budgets alone.\n\n"
        )

        f.write(
            "The U.S. Department of State's Bureau of Counterterrorism describes modern "
            "counterterrorism as involving diplomacy, multilateral cooperation, civilian "
            "capacity-building, border and aviation security, sanctions and terrorist "
            "designations, countering violent extremism, and partner support. This shows "
            "that counterterrorism is partly military, but also institutional, diplomatic, "
            "financial, legal, and law-enforcement oriented.\n\n"
        )

        f.write(
            "Brown University's Costs of War project also demonstrates the breadth of "
            "counterterrorism activity. Its report on U.S. counterterrorism operations from "
            "2021 to 2023 documents activity in 78 countries, including training and "
            "assistance in 73 countries, ground combat in at least nine countries, and air "
            "or drone strikes in four to five countries. This supports the interpretation "
            "that military expenditure is a broad proxy rather than a precise measure of "
            "counterterrorism spending.\n\n"
        )

        f.write("## Variables\n\n")
        f.write("### Dependent Variables\n\n")
        f.write("- Terrorist attacks per country-year\n")
        f.write("- Terrorism deaths per country-year\n")
        f.write("- Log terrorist attacks\n")
        f.write("- Log terrorism deaths\n\n")

        f.write("### Main Independent Variable\n\n")
        f.write(
            "- Lagged log military spending, measured as prior-year military expenditure. "
            "The lagged variable is used to reduce same-year reverse-causality concerns.\n\n"
        )

        f.write("### Control Variables\n\n")
        f.write("- GDP\n")
        f.write("- Population\n")
        f.write("- Year fixed effects\n")
        f.write("- Country fixed effects in the stronger panel models\n\n")

        f.write("## Descriptive Findings\n\n")
        f.write(
            "The descriptive charts show that global terrorist attacks and terrorism deaths "
            "rose sharply after 2011, peaked around 2014, and then declined through the end "
            "of the study period. Terrorism was also highly concentrated geographically. "
            "Iraq and Afghanistan were the most affected countries by total attacks, while "
            "Iraq, Afghanistan, Nigeria, Pakistan, and Syria were among the countries with "
            "the highest terrorism-related death totals.\n\n"
        )

        f.write(
            "The scatterplots comparing military spending and terrorism outcomes do not show "
            "a simple negative relationship. In other words, countries with higher military "
            "spending do not clearly experience fewer attacks or fewer deaths in the raw visual "
            "patterns. This supports the need for regression models that control for GDP, "
            "population, year effects, and country-level differences.\n\n"
        )

        f.write("## Key Charts Created\n\n")
        for chart in chart_list:
            chart_path = CHART_DIR / chart
            if chart_path.exists():
                f.write(f"- `{chart}`\n")
        f.write("\n")

        f.write("## Regression Approach\n\n")
        f.write(
            "The regression analysis compares two types of models. The first set includes "
            "year fixed effects only. These models compare countries to one another while "
            "controlling for global year-specific shocks. The second set includes both "
            "country and year fixed effects. These stronger panel models compare each country "
            "more closely against itself over time, reducing bias from stable differences "
            "between countries.\n\n"
        )

        f.write("## Regression Findings\n\n")
        f.write(
            "The regression results show that model specification strongly affects the "
            "relationship between military spending and terrorism outcomes. In the basic "
            "models with year fixed effects only, lagged military spending is positively "
            "and statistically significantly associated with both terrorist attacks and "
            "terrorism deaths. However, after adding country fixed effects, the coefficient "
            "on lagged military spending becomes small and statistically insignificant.\n\n"
        )

        f.write(
            "| Model | Outcome | Coefficient | Standard Error | P-value | Significant? |\n"
        )
        f.write("|---|---|---:|---:|---:|---|\n")

        for _, row in regression_results.iterrows():
            significant = "Yes" if row["statistically_significant"] else "No"
            f.write(
                f"| {row['model']} | {row['outcome']} | "
                f"{row['coefficient']:.4f} | "
                f"{row['standard_error']:.4f} | "
                f"{format_p_value(row['p_value'])} | "
                f"{significant} |\n"
            )

        f.write("\n")

        f.write(
            "This pattern suggests that the positive relationship in the basic models is "
            "likely driven by cross-country differences. Countries facing greater terrorism "
            "risk also tend to spend more on defense and security. Once countries are "
            "compared more closely against their own historical patterns, lagged military "
            "spending is not a statistically significant predictor of later terrorism "
            "outcomes.\n\n"
        )

        f.write("## Discussion\n\n")
        f.write(
            "The most important finding is that the relationship between military spending "
            "and terrorism outcomes changes substantially after country fixed effects are "
            "included. In the basic models, lagged military spending is positively and "
            "statistically significantly associated with terrorist attacks and terrorism "
            "deaths. However, once country fixed effects are added, the coefficient becomes "
            "small and statistically insignificant for both outcomes.\n\n"
        )

        f.write(
            "This suggests that the positive relationship in the basic models is likely "
            "driven by differences between countries. Countries facing greater terrorism "
            "risk tend to spend more on defense and security, so cross-country comparisons "
            "can make spending appear positively associated with terrorism. When countries "
            "are compared more closely against their own historical patterns, military "
            "spending does not appear to be a statistically significant predictor of later "
            "terrorism outcomes.\n\n"
        )

        f.write("## Limitations\n\n")
        f.write(
            "There are several important limitations. First, military expenditure is an "
            "imperfect proxy for counterterrorism spending. It includes broad defense spending "
            "and does not isolate spending specifically directed toward terrorism prevention, "
            "intelligence, law enforcement, border security, homeland security, sanctions "
            "enforcement, foreign assistance, or civilian capacity-building.\n\n"
        )

        f.write(
            "Second, the study does not fully measure domestic law enforcement, intelligence, "
            "homeland security, or foreign aid programs aimed at counterterrorism. Third, the "
            "analysis is observational, so it cannot prove causation. Fourth, terrorism data "
            "may be affected by reporting differences across countries and years. Finally, "
            "countries often increase security spending in response to terrorism threats, "
            "making reverse causality a central concern.\n\n"
        )

        f.write(
            "These limitations are especially important because recent counterterrorism "
            "policy documents show that counterterrorism activity includes a wide range of "
            "tools beyond military operations. State Department reporting emphasizes civilian "
            "capacity-building, border security, diplomacy, multilateral coordination, and "
            "partner support, while Costs of War research documents global U.S. counterterrorism "
            "activity across training, assistance, combat, and air or drone operations.\n\n"
        )

        f.write("## Future Research\n\n")
        f.write(
            "Future research could improve on this study by using more detailed "
            "counterterrorism-specific spending measures. Rather than relying only on aggregate "
            "military expenditure, a future project could separate defense spending, homeland "
            "security spending, foreign assistance, border security programs, intelligence-related "
            "spending, counterterrorism training, sanctions enforcement, and civilian "
            "capacity-building.\n\n"
        )

        f.write(
            "A U.S.-focused extension could also use sources such as USAspending.gov, "
            "Department of Defense budget documents, Department of Homeland Security budget "
            "documents, State Department counterterrorism foreign assistance data, and Costs "
            "of War estimates to create a more detailed spending dataset. This would allow "
            "researchers to examine whether some types of counterterrorism spending are more "
            "closely associated with changes in terrorist attacks and terrorism-related deaths "
            "than others.\n\n"
        )

        f.write("## Conclusion\n\n")
        f.write(
            "Overall, the results do not provide evidence that higher military spending "
            "reduces terrorist attacks or terrorism deaths. The basic models show a positive "
            "association between lagged military spending and terrorism outcomes, but this "
            "relationship disappears in the stronger country fixed effects models. The findings "
            "therefore suggest that cross-country differences in terrorism risk explain much of "
            "the apparent relationship between spending and terrorism. A more precise study of "
            "counterterrorism effectiveness would require narrower data on actual counterterrorism, "
            "intelligence, policing, border security, foreign assistance, civilian capacity-building, "
            "and prevention expenditures.\n\n"
        )

        f.write("## References\n\n")
        f.write(
            "- Brown University, Watson Institute for International and Public Affairs. "
            "Costs of War Project. *United States Counterterrorism Operations, 2021–2023*.\n"
        )
        f.write(
            "- United Nations Office of Counter-Terrorism. *Funding and Donors*.\n"
        )
        f.write(
            "- United States Department of State, Bureau of Counterterrorism. "
            "*2022 Annual Report*.\n"
        )
        f.write(
            "- The White House. *United States Counterterrorism Strategy, 2026*.\n"
        )
        f.write(
            "- USAspending.gov. *Department of Defense Agency Profile*.\n"
        )
        f.write(
            "- World Bank. *World Development Indicators*.\n"
        )
        f.write(
            "- Stockholm International Peace Research Institute. *Military Expenditure Data*.\n"
        )
        f.write(
            "- Global Terrorism Database. *National Consortium for the Study of Terrorism "
            "and Responses to Terrorism*.\n"
        )

    print(f"Saved final report to {report_path}")


if __name__ == "__main__":
    create_final_report()