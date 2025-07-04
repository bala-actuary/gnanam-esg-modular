import numpy as np
from scipy.stats import norm
from .formulas import d1, d2


def calculate_default_probability(
    asset_value, asset_volatility, face_value_debt, time_to_maturity, risk_free_rate
):
    """Calculates the default probability using the Merton Model."""
    # Distance to default (d2 in Black-Scholes for a put option)
    # Here, S is Asset Value, K is Face Value of Debt, sigma is Asset Volatility
    d2_val = d2(
        asset_value, face_value_debt, time_to_maturity, risk_free_rate, asset_volatility
    )
    return norm.cdf(-d2_val)


def calculate_credit_spread(
    asset_value, asset_volatility, face_value_debt, time_to_maturity, risk_free_rate
):
    """Calculates the credit spread using the Merton Model."""
    # This is an approximation. A more precise calculation involves solving for the yield.
    # For simplicity, we'll use the formula: Credit Spread = -1/T * ln(P_debt / F)
    # where P_debt is the market value of debt.
    # P_debt = F * exp(-rT) - Equity_Put_Option_Price
    # Equity_Put_Option_Price = K * exp(-rT) * N(-d2) - S * N(-d1)
    # In Merton, Equity is a call option on Assets, Debt is a put option on Assets.
    # Value of Debt = Face_Value_Debt * exp(-rT) - Asset_Put_Option_Price

    # For now, a simplified approach based on PD and recovery rate (assuming 0 recovery for simplicity)
    # This needs to be refined for a proper credit spread calculation.
    # A common approximation: CS = -1/T * ln(1 - PD)
    # This is not strictly correct for Merton, but provides a placeholder.

    # Let's use the more direct approach from the Merton model for debt value
    # Value of Debt = V_A * N(-d1) + F * exp(-rT) * N(d2)
    # where d1 and d2 are based on Asset Value (V_A) and Asset Volatility (sigma_A)

    d1_val = d1(
        asset_value, face_value_debt, time_to_maturity, risk_free_rate, asset_volatility
    )
    d2_val = d2(
        asset_value, face_value_debt, time_to_maturity, risk_free_rate, asset_volatility
    )

    value_of_debt = asset_value * norm.cdf(-d1_val) + face_value_debt * np.exp(
        -risk_free_rate * time_to_maturity
    ) * norm.cdf(d2_val)

    # Credit Spread = -1/T * ln(Value_of_Debt / Face_Value_Debt)
    if value_of_debt <= 0 or face_value_debt <= 0:
        return np.nan  # Avoid log of non-positive numbers

    credit_spread = -(1 / time_to_maturity) * np.log(value_of_debt / face_value_debt)
    return credit_spread
