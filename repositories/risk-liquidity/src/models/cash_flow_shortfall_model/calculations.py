import pandas as pd


def calculate_net_cash_flow(inflows: pd.Series, outflows: pd.Series) -> pd.Series:
    """Calculates net cash flow for each period."""
    return inflows - outflows


def calculate_cumulative_cash_flow(net_cash_flow: pd.Series) -> pd.Series:
    """Calculates cumulative net cash flow."""
    return net_cash_flow.cumsum()


def identify_shortfalls(cumulative_cash_flow: pd.Series) -> pd.Series:
    """Identifies periods with liquidity shortfalls."""
    return cumulative_cash_flow < 0
