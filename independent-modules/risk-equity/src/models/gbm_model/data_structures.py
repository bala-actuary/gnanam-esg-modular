from dataclasses import dataclass
import numpy as np


@dataclass
class GBMInputData:
    """Data container for the input parameters of the GBM Model."""

    initial_price: float
    expected_return: float
    volatility: float
    time_horizon: float
    num_time_steps: int
    num_paths: int


@dataclass
class GBMSimulationResult:
    """Data container for the results of a GBM simulation."""

    paths: np.ndarray  # Shape: (num_time_steps + 1, num_paths)
    time_grid: np.ndarray  # The time steps used in the simulation
