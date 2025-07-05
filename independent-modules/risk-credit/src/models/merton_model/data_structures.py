from dataclasses import dataclass
import numpy as np


@dataclass
class MertonInputData:
    """Data container for the input parameters of the Merton Model."""

    equity_value: float
    equity_volatility: float
    face_value_debt: float
    time_to_maturity: float
    risk_free_rate: float


@dataclass
class CalibratedMertonModel:
    """Data container for the calibrated parameters of the Merton Model."""

    asset_value: float
    asset_volatility: float


@dataclass
class MertonOutputResults:
    """Data container for the output results of the Merton Model."""

    default_probability: float
    credit_spread: float


@dataclass
class MertonSimulationResult:
    """Data container for the results of a Merton simulation."""

    paths: np.ndarray  # Shape: (num_time_steps + 1, num_paths)
    time_grid: np.ndarray  # The time steps used in the simulation
    default_events: np.ndarray  # Boolean array indicating default at each step
