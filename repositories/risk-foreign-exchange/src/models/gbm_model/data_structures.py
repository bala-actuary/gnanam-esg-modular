from dataclasses import dataclass
import numpy as np


@dataclass
class FXGBMInputData:
    """Data container for the input parameters of the FX GBM Model."""

    initial_exchange_rate: float
    domestic_risk_free_rate: float
    foreign_risk_free_rate: float
    volatility: float
    time_horizon: float
    num_time_steps: int
    num_paths: int


@dataclass
class FXGBMSimulationResult:
    """Data container for the results of an FX GBM simulation."""

    paths: np.ndarray  # Shape: (num_time_steps + 1, num_paths)
    time_grid: np.ndarray  # The time steps used in the simulation
