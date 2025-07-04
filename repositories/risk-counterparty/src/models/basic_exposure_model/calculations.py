import pandas as pd


def calculate_counterparty_exposures(portfolio_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates total, positive, and negative exposures per counterparty."""
    # Group by Counterparty_ID and sum market values
    grouped = portfolio_df.groupby("Counterparty_ID")["Market_Value"]

    total_exposure = grouped.sum().reset_index()
    total_exposure.rename(columns={"Market_Value": "Total_Exposure"}, inplace=True)

    # Calculate positive exposure
    positive_exposure = (
        portfolio_df[portfolio_df["Market_Value"] > 0]
        .groupby("Counterparty_ID")["Market_Value"]
        .sum()
        .reset_index()
    )
    positive_exposure.rename(
        columns={"Market_Value": "Positive_Exposure"}, inplace=True
    )

    # Calculate negative exposure
    negative_exposure = (
        portfolio_df[portfolio_df["Market_Value"] < 0]
        .groupby("Counterparty_ID")["Market_Value"]
        .sum()
        .reset_index()
    )
    negative_exposure.rename(
        columns={"Market_Value": "Negative_Exposure"}, inplace=True
    )

    # Merge all exposures
    results_df = total_exposure.merge(
        positive_exposure, on="Counterparty_ID", how="left"
    )
    results_df = results_df.merge(negative_exposure, on="Counterparty_ID", how="left")

    # Fill NaN with 0 for counterparties with no positive or negative exposures
    results_df.fillna(0, inplace=True)

    return results_df
