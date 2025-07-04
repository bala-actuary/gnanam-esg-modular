from dataclasses import dataclass
import numpy as np


@dataclass
class InflationInputData:
    """Data container for the input parameters of the Mean-Reverting Inflation Model."""

    initial_inflation_rate: float
    long_term_mean_inflation_rate: float
    mean_reversion_speed: float
    volatility: float
    time_horizon: float
    num_time_steps: int
    num_paths: int


@dataclass
class InflationSimulationResult:
    """Data container for the results of an Inflation simulation."""

    paths: np.ndarray  # Shape: (num_time_steps + 1, num_paths)
    time_grid: np.ndarray  # The time steps used in the simulation
