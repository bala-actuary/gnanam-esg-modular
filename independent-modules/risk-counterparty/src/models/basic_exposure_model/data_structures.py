from dataclasses import dataclass
import pandas as pd


@dataclass
class TradePortfolioInputData:
    """Data container for the input trade portfolio data."""

    portfolio_df: pd.DataFrame  # DataFrame with Counterparty_ID, Trade_ID, Market_Value


@dataclass
class ExposureResults:
    """Data container for the calculated exposure results."""

    results_df: (
        pd.DataFrame
    )  # DataFrame with Counterparty_ID, Total_Exposure, Positive_Exposure, Negative_Exposure
