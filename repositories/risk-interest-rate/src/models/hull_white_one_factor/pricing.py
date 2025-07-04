from . import formulas
from .data_structures import CalibratedHW1FModel
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq  # For root finding


def price_zcb(
    t: float, T: float, r_t: float, calibrated_model: CalibratedHW1FModel
) -> float:
    """Prices a Zero-Coupon Bond using the analytical formula.
    P(t,T) = A(t,T) * exp(-B(t,T) * r_t)
    """
    A_t_T = formulas.A(t, T, calibrated_model)
    B_t_T = formulas.B(t, T, calibrated_model.a)
    return A_t_T * np.exp(-B_t_T * r_t)


def price_european_option_on_zcb(
    K: float,
    T: float,
    S: float,
    calibrated_model: CalibratedHW1FModel,
    option_type: str = "call",
) -> float:
    """Prices a European option on a Zero-Coupon Bond.
    K: Strike price
    T: Expiry of the option
    S: Maturity of the underlying ZCB
    calibrated_model: Calibrated Hull-White model
    option_type: 'call' or 'put'
    """
    a = calibrated_model.a
    sigma = calibrated_model.sigma

    # P(t,S) is the price of a ZCB at time t maturing at S
    # P(t,T) is the price of a ZCB at time t maturing at T (option expiry)
    # We need P(0,S) and P(0,T) from the initial curve
    P0S = calibrated_model.initial_zero_coupon_bond_pricer(S)
    P0T = calibrated_model.initial_zero_coupon_bond_pricer(T)

    sigma_p = sigma * np.sqrt((1 - np.exp(-2 * a * T)) / (2 * a)) * formulas.B(T, S, a)

    h = (np.log(P0S / (P0T * K)) + 0.5 * sigma_p**2) / sigma_p

    if option_type == "call":
        price = P0S * norm.cdf(h) - K * P0T * norm.cdf(h - sigma_p)
    elif option_type == "put":
        price = K * P0T * norm.cdf(sigma_p - h) - P0S * norm.cdf(-h)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    return price


def price_european_swaption(
    swap_rate: float,
    expiry: float,
    tenor_start: float,
    tenor_end: float,
    fixed_frequency: float,
    calibrated_model: CalibratedHW1FModel,
    option_type: str = "payer",
) -> float:
    """Prices a European swaption using Jamshidian's Trick.
    swap_rate: The fixed rate of the underlying swap
    expiry: The expiry of the swaption (time T)
    tenor_start: The start of the swap tenor (time T_alpha)
    tenor_end: The end of the swap tenor (time T_beta)
    fixed_frequency: Frequency of fixed payments (e.g., 0.5 for semi-annual)
    calibrated_model: Calibrated Hull-White model
    option_type: 'payer' or 'receiver'
    """
    # Jamshidian's Trick involves finding a critical short rate r* at expiry (T)
    # such that the present value of the fixed leg equals the present value of the floating leg.
    # Then, the swaption is decomposed into a portfolio of options on zero-coupon bonds.

    # 1. Define the fixed leg payment dates and corresponding ZCB maturities
    fixed_payment_dates = np.arange(
        tenor_start, tenor_end + fixed_frequency, fixed_frequency
    )
    fixed_payment_dates = fixed_payment_dates[
        fixed_payment_dates > expiry
    ]  # Only payments after expiry

    if len(fixed_payment_dates) == 0:
        return 0.0  # No payments after expiry, swaption is worthless

    # 2. Define the objective function for finding the critical rate r*
    # The objective is to find r* such that the PV of the fixed leg equals the PV of the floating leg at expiry T
    # PV_fixed = sum(delta_i * K * P(T, T_i, r*))
    # PV_floating = P(T, T_alpha, r*) - P(T, T_beta, r*)
    # where P(T, T_i, r*) is the ZCB price at time T for maturity T_i, given short rate r*

    def swap_pv_at_expiry(r_star: float) -> float:
        pv_fixed = 0.0
        for t_i in fixed_payment_dates:
            delta_i = fixed_frequency  # Assuming constant frequency
            pv_fixed += (
                delta_i * swap_rate * price_zcb(expiry, t_i, r_star, calibrated_model)
            )

        pv_floating = price_zcb(
            expiry, tenor_start, r_star, calibrated_model
        ) - price_zcb(expiry, tenor_end, r_star, calibrated_model)
        return pv_fixed - pv_floating

    # 3. Find the critical rate r* using a root-finding algorithm
    # We need to provide a bracket [a, b] where swap_pv_at_expiry(a) and swap_pv_at_expiry(b) have opposite signs.
    # This can be tricky. For now, we'll use a wide range and assume a root exists.
    # In a real scenario, this might need more robust handling or an initial guess.
    try:
        r_star = brentq(
            swap_pv_at_expiry, -0.5, 0.5
        )  # Search between -50% and 50% short rate
    except ValueError:
        # If no root is found in the interval, the swaption might be deep in/out of the money
        # or the interval is too small. For simplicity, return 0 or handle as appropriate.
        return 0.0  # Placeholder for now

    # 4. Decompose the swaption into a portfolio of options on ZCBs
    swaption_price = 0.0
    for t_i in fixed_payment_dates:
        delta_i = fixed_frequency
        # The option on ZCB is struck at P(T, T_i, r*) = K_i
        # K_i = price_zcb(expiry, t_i, r_star, calibrated_model)
        # The underlying is P(T, T_i, r_T) where r_T is the actual short rate at expiry

        # The option is on the ZCB P(expiry, t_i) with strike price K_i = price_zcb(expiry, t_i, r_star, calibrated_model)
        # The option type depends on the swaption type
        if (
            option_type == "payer"
        ):  # Payer swaption: option to pay fixed, receive float. Equivalent to call on ZCBs.
            # For a payer swaption, we are long the floating leg and short the fixed leg.
            # This is equivalent to a portfolio of call options on ZCBs.
            # The strike for each ZCB option is the ZCB price at expiry corresponding to r_star.
            strike_zcb = price_zcb(expiry, t_i, r_star, calibrated_model)
            swaption_price += (
                delta_i
                * swap_rate
                * price_european_option_on_zcb(
                    strike_zcb, expiry, t_i, calibrated_model, "call"
                )
            )
        elif (
            option_type == "receiver"
        ):  # Receiver swaption: option to receive fixed, pay float. Equivalent to put on ZCBs.
            # For a receiver swaption, we are short the floating leg and long the fixed leg.
            # This is equivalent to a portfolio of put options on ZCBs.
            strike_zcb = price_zcb(expiry, t_i, r_star, calibrated_model)
            swaption_price += (
                delta_i
                * swap_rate
                * price_european_option_on_zcb(
                    strike_zcb, expiry, t_i, calibrated_model, "put"
                )
            )
        else:
            raise ValueError("option_type must be 'payer' or 'receiver'")

    return swaption_price
