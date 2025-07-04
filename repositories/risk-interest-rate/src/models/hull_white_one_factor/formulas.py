import numpy as np
from .data_structures import CalibratedHW1FModel


def B(t: float, T: float, a: float) -> float:
    """Calculates the B(t,T) term of the HW1F model."""
    if a == 0:
        return T - t
    return (1 / a) * (1 - np.exp(-a * (T - t)))


def instantaneous_forward_rate(t_val: float, p0_pricer: callable) -> float:
    """Calculates the instantaneous forward rate f(0,t) from zero-coupon bond prices."""
    eps = 1e-5
    if t_val < eps:
        # Handle t=0 case or very small t
        return -(np.log(p0_pricer(t_val + eps)) - np.log(p0_pricer(t_val))) / eps
    else:
        return -(np.log(p0_pricer(t_val + eps)) - np.log(p0_pricer(t_val - eps))) / (
            2 * eps
        )


def A(t: float, T: float, calibrated_model: CalibratedHW1FModel) -> float:
    """Calculates the A(t,T) term of the HW1F model.
    This function requires the theta_function from the calibrated model
    and implicitly relies on the initial yield curve used for calibration.
    """
    a = calibrated_model.a
    sigma = calibrated_model.sigma
    P0T = calibrated_model.initial_zero_coupon_bond_pricer(T)
    P0t = calibrated_model.initial_zero_coupon_bond_pricer(t)

    f0t = instantaneous_forward_rate(
        t, calibrated_model.initial_zero_coupon_bond_pricer
    )

    B_t_T = B(t, T, a)
    term = B_t_T * f0t - (sigma**2 / (4 * a)) * (1 - np.exp(-2 * a * t)) * B_t_T
    return (P0T / P0t) * np.exp(term)


def generate_theta_function(
    a: float, sigma: float, initial_zero_coupon_bond_pricer: callable
) -> callable:
    """Generates the theta(t) function for the Hull-White model that fits the initial term structure."""

    def derivative_of_instantaneous_forward_rate(t_val: float) -> float:
        eps = 1e-5
        return (
            instantaneous_forward_rate(t_val + eps, initial_zero_coupon_bond_pricer)
            - instantaneous_forward_rate(t_val - eps, initial_zero_coupon_bond_pricer)
        ) / (2 * eps)

    def theta(t: float) -> float:
        f_0_t = instantaneous_forward_rate(t, initial_zero_coupon_bond_pricer)
        df_0_t = derivative_of_instantaneous_forward_rate(t)
        return df_0_t + a * f_0_t + (sigma**2 / (2 * a)) * (1 - np.exp(-2 * a * t))

    return theta
