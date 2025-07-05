from dataclasses import dataclass
import pandas as pd


@dataclass
class CashFlowInputData:
    """Data container for the input cash flow data."""

    cash_flows_df: pd.DataFrame  # DataFrame with Date, Inflows, Outflows


@dataclass
class CashFlowResults:
    """Data container for the calculated cash flow results."""

    results_df: (
        pd.DataFrame
    )  # DataFrame with Date, Inflows, Outflows, Net_Cash_Flow, Cumulative_Cash_Flow, Shortfall
