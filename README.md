# Counterterrorism Spending and Terrorist Attack Severity

A Python-based country-year panel study analyzing the relationship between military expenditure and terrorism outcomes from 2001 to 2020.

## Project Overview

This project examines whether higher prior-year military/security spending is associated with fewer terrorist attacks or fewer terrorism-related deaths.

The analysis combines terrorism event data from the Global Terrorism Database with World Bank/SIPRI military expenditure, GDP, and population indicators. The final model dataset includes 1,382 country-year observations.

The project uses Python to collect data, process country-year terrorism indicators, merge macroeconomic and military spending data, generate visualizations, and estimate regression models with year fixed effects and country + year fixed effects.

## Research Question

Does higher prior-year military spending predict fewer terrorist attacks or terrorism-related deaths?

## Data Sources

- Global Terrorism Database: terrorist attacks, deaths, wounded, casualties, and country-year terrorism totals
- World Bank / SIPRI indicators:
  - Military expenditure, current US$
  - Military expenditure as percent of GDP
  - GDP, current US$
  - Population

## Key Variables

### Dependent Variables

- Terrorist attacks per country-year
- Terrorism deaths per country-year
- Wounded per country-year
- Casualties per country-year
- Log terrorist attacks
- Log terrorism deaths

### Main Independent Variable

- Lagged log military expenditure, measured at t-1

### Controls

- GDP
- Population
- Year fixed effects
- Country fixed effects in the stronger panel models

## Methodology

The project estimates two sets of regression models:

1. **Year fixed effects models**  
   These compare countries to one another while controlling for global year-specific shocks.

2. **Country and year fixed effects models**  
   These compare each country more closely against itself over time, reducing bias from stable country-level differences.

The key predictor is lagged military spending, which is used to reduce same-year reverse-causality concerns.

## Key Findings

The basic year fixed effects models show a positive and statistically significant association between lagged military spending and terrorism outcomes.

However, after adding country fixed effects, the relationship becomes small and statistically insignificant for both terrorist attacks and terrorism deaths.

This suggests the initial positive relationship is likely driven by cross-country differences in terrorism risk. Countries facing greater terrorism risk also tend to spend more on defense and security, but within-country changes in spending do not significantly predict later terrorism outcomes.

## Regression Summary

| Model | Outcome | Coefficient | Standard Error | P-value | Significant? |
|---|---|---:|---:|---:|---|
| Year FE | Log terrorist attacks | 0.1043 | 0.0208 | 5.361e-07 | Yes |
| Year FE | Log terrorism deaths | 0.1196 | 0.0269 | 8.507e-06 | Yes |
| Country + Year FE | Log terrorist attacks | -0.0026 | 0.0265 | 0.9232 | No |
| Country + Year FE | Log terrorism deaths | -0.0301 | 0.0451 | 0.5039 | No |

## Important Limitation

Military expenditure is only a broad proxy for counterterrorism spending. It includes broader defense spending and does not isolate spending specifically used for counterterrorism, intelligence, policing, homeland security, border security, sanctions enforcement, foreign assistance, or civilian capacity-building.

The results should therefore be interpreted as evidence about military spending and terrorism outcomes, not as a direct causal estimate of counterterrorism program effectiveness.

## Repository Structure

```text
counterterrorism-spending-study/
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
│   ├── charts/
│   ├── final_report.md
│   ├── results_summary.md
│   ├── regression_results.txt
│   └── summary_statistics.csv
├── src/
│   ├── analysis.py
│   ├── config.py
│   ├── gtd_processing.py
│   ├── merge_data.py
│   ├── report_generator.py
│   ├── results_summary.py
│   ├── visualization.py
│   └── worldbank_api.py
├── main.py
├── requirements.txt
└── README.md
```

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the full GTD Excel file in:

```text
data/raw/globalterrorismdb.xlsx
```

Run the full pipeline:

```bash
python main.py
```

## Outputs

The pipeline creates:

- Processed country-year panel dataset
- Summary statistics
- Regression results
- Key coefficient table
- Results summary
- Final markdown report
- Charts showing terrorism trends, country concentration, and spending relationships

## Notes on Data Access

The Global Terrorism Database file is not included in this repository. Users should download the GTD dataset themselves from the START Global Terrorism Database (https://www.start.umd.edu/gtd/), subject to its terms of use, and place it in the `data/raw/` folder as `globalterrorismdb.xlsx`.

Processed datasets are also excluded from version control to keep the repository lightweight and reproducible.

## Tools Used

- Python
- pandas
- NumPy
- matplotlib
- statsmodels
- World Bank API

## Author

Jason Keen  
[LinkedIn](https://www.linkedin.com/in/jason-keen-1887b4218)
