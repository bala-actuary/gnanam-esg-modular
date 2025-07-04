from dataclasses import dataclass
import numpy as np


@dataclass
class CalibratedHW1FModel:
    """Data container for the results of a successful calibration."""

    a: float  # Mean reversion speed
    sigma: float  # Volatility
    theta_function: callable  # The determined theta function (t -> theta(t))
    calibration_error: float
    initial_zero_coupon_bond_pricer: (
        callable  # A function P(0,t) -> price, derived from the initial yield curve
    )


@dataclass
class HW1FSimulationResult:
    """Data container for the results of a simulation."""

    paths: np.ndarray  # Shape: (num_timesteps, num_paths)
    time_grid: np.ndarray  # The time steps used in the simulation
