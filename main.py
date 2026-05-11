from src.worldbank_api import build_worldbank_dataset
from src.gtd_processing import build_gtd_country_year
from src.merge_data import merge_panel_data
from src.analysis import run_analysis
from src.visualization import build_charts
from src.results_summary import create_results_summary
from src.report_generator import create_final_report


def main():
    print("Building World Bank dataset...")
    build_worldbank_dataset()

    print("\nProcessing Global Terrorism Database...")
    build_gtd_country_year()

    print("\nMerging panel dataset...")
    merge_panel_data()

    print("\nRunning regression analysis...")
    run_analysis()

    print("\nBuilding charts...")
    build_charts()

    print("\nCreating written results summary...")
    create_results_summary()

    print("\nCreating final report...")
    create_final_report()

    print("\nProject complete.")
    print("\nKey outputs:")
    print("- data/processed/terrorism_spending_panel.csv")
    print("- outputs/summary_statistics.csv")
    print("- outputs/regression_results.txt")
    print("- outputs/results_summary.md")
    print("- outputs/final_report.md")
    print("- outputs/charts/")


if __name__ == "__main__":
    main()