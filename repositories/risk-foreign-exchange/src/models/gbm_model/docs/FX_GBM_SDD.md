# Software Design Document (SDD)
### Model Plugin: Geometric Brownian Motion (GBM) Model for Foreign Exchange Risk
**Version:** 1.0
**Date:** 28 June 2025

## 1. Introduction

#### 1.1 Purpose
This document provides the detailed software design for the **Geometric Brownian Motion (GBM) Model Plugin** for Foreign Exchange Risk. It is the technical implementation plan for the requirements specified in `FX_GBM_SRS.md` and is designed to conform to the master `PLATFORM_ARCHITECTURE.md`.

#### 1.2 Scope
This design covers the internal structure of the FX GBM Model plugin, including its primary class, data structures, core algorithms for simulation, and its data interface with the file system.

## 2. High-Level Design

#### 2.1 Architectural Approach
The plugin will be developed as a self-contained Python package within the `src/models/Foreign_Exchange_Risk/gbm_model/` directory. The design will be centered around a main `FXGBMModel` class. Helper functions for mathematical formulas will be separated into their own modules for clarity and testability.

#### 2.2 Module Structure
```
/gbm_model/
|-- docs/
|   |-- FX_GBM_SRS.md
|   `-- FX_GBM_SDD.md
|
|-- __init__.py
|-- model.py          # Contains the main FXGBMModel class.
|-- formulas.py       # Contains pure mathematical functions (e.g., GBM process equation).
`-- data_structures.py # Defines data classes for inputs and outputs.
```

#### 2.3 Data Interface (File-Based)
To decouple the model logic from data management, the plugin will interact with the file system for its primary inputs and outputs. This allows for easier testing, data versioning, and integration into larger workflows.

*   **Input Directory:** `RiskModels/data/inputs/fx_gbm_model/`
    *   `fx_gbm_parameters.csv`: Contains the input data for FX GBM parameters. Columns: `Initial_Exchange_Rate`, `Domestic_Risk_Free_Rate`, `Foreign_Risk_Free_Rate`, `Volatility`, `Time_Horizon`, `Num_Time_Steps`, `Num_Paths`.
*   **Output Directory:** `RiskModels/data/outputs/fx_gbm_model/`
    *   `simulated_exchange_rates.csv`: Stores the primary output of the simulation (simulated exchange rate paths).
    *   `simulated_exchange_rate_paths.html`: Interactive HTML plot visualizing simulated exchange rate paths.
    *   `exchange_rate_distribution_at_maturity.html`: Interactive HTML plot showing the distribution of exchange rates at maturity.


## 3. Detailed Component Design

### 3.1. Data Structures (`data_structures.py`)
We will use Python's `dataclasses` for creating simple, typed data containers.

```python
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
    time_grid: np.ndarray # The time steps used in the simulation

# Data loading will be handled within the model.py module, which will
# read the CSV files and construct the necessary internal data representations.
```

### 3.2. Mathematical Formulas (`formulas.py`)
This module will contain pure, stateless functions for the core FX GBM mathematical components.

```python
import numpy as np

def fx_gbm_step(S_t, r_d, r_f, sigma, dt, dW):
    """Calculates one step of the FX GBM process."""
    pass
```

### 3.3. Main Plugin Class (`model.py`)
This is the public-facing class of the plugin, implementing the `ModelInterface`.

```python
from . import formulas
from .data_structures import FXGBMInputData, FXGBMSimulationResult
import pandas as pd
import os
import numpy as np

# Assume ModelInterface is imported from the Core Engine
class FXGBMModel(ModelInterface):

    def __init__(self, input_dir="RiskModels/data/inputs/fx_gbm_model", output_dir="RiskModels/data/outputs/fx_gbm_model"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_name(self) -> str:
        return "fx_gbm_model"

    def get_required_risk_factors(self) -> list[str]:
        return ["initial_exchange_rate", "domestic_risk_free_rate", "foreign_risk_free_rate", "volatility", "time_horizon", "num_time_steps", "num_paths"]

    # --- Public Methods (for file-based I/O and convenience) ---

    def simulate(self, scenario_definition: dict, correlated_shocks=None, plot_options: dict = None) -> FXGBMSimulationResult:
        input_data = self._load_and_prepare_data(scenario_definition) # scenario_definition can override file data
        simulation_result = self._simulate_logic(input_data, correlated_shocks)

        # Convert simulation results to a DataFrame for consistent output and plotting
        simulation_df = pd.DataFrame(simulation_result.paths, index=simulation_result.time_grid)
        simulation_df.index.name = 'Time'
        simulation_df.reset_index(inplace=True)
        simulation_df.columns = ['Time'] + [f'Path_{i}' for i in range(input_data.num_paths)]

        # Save results to CSV
        output_path_csv = os.path.join(self.output_dir, "simulated_exchange_rates.csv")
        simulation_df.to_csv(output_path_csv, index=False)

        # Generate and save plots based on plot_options
        if plot_options is None:
            plot_options = {
                "exchange_rate_paths": {"enabled": True},
                "exchange_rate_distribution_at_maturity": {"enabled": True}
            }

        from visualization.plotter import plot_exchange_rate_paths, plot_exchange_rate_distribution_at_maturity

        if plot_options.get("exchange_rate_paths", {}).get("enabled", False):
            output_filename = plot_options["exchange_rate_paths"].get("output_filename", "simulated_exchange_rate_paths.html")
            plot_exchange_rate_paths(
                simulation_df,
                os.path.join(self.output_dir, output_filename)
            )

        if plot_options.get("exchange_rate_distribution_at_maturity", {}).get("enabled", False):
            output_filename = plot_options["exchange_rate_distribution_at_maturity"].get("output_filename", "exchange_rate_distribution_at_maturity.html")
            plot_exchange_rate_distribution_at_maturity(
                simulation_df,
                os.path.join(self.output_dir, output_filename)
            )

        return simulation_result

    # --- Internal Logic Methods (for pure in-memory operations) ---

    def _load_and_prepare_data(self, scenario_definition: dict) -> FXGBMInputData:
        # Load data from CSV file, but allow scenario_definition to override
        fx_gbm_data_path = os.path.join(self.input_dir, "fx_gbm_parameters.csv")
        df = pd.read_csv(fx_gbm_data_path)
        
        # Use values from scenario_definition if provided, otherwise from CSV
        return FXGBMInputData(
            initial_exchange_rate=scenario_definition.get('initial_exchange_rate', df['Initial_Exchange_Rate'].iloc[0]),
            domestic_risk_free_rate=scenario_definition.get('domestic_risk_free_rate', df['Domestic_Risk_Free_Rate'].iloc[0]),
            foreign_risk_free_rate=scenario_definition.get('foreign_risk_free_rate', df['Foreign_Risk_Free_Rate'].iloc[0]),
            volatility=scenario_definition.get('volatility', df['Volatility'].iloc[0]),
            time_horizon=scenario_definition.get('time_horizon', df['Time_Horizon'].iloc[0]),
            num_time_steps=scenario_definition.get('num_time_steps', df['Num_Time_Steps'].iloc[0]),
            num_paths=scenario_definition.get('num_paths', df['Num_Paths'].iloc[0])
        )

    def _simulate_logic(self, input_data: FXGBMInputData, correlated_shocks=None) -> FXGBMSimulationResult:
        S0 = input_data.initial_exchange_rate
        r_d = input_data.domestic_risk_free_rate
        r_f = input_data.foreign_risk_free_rate
        sigma = input_data.volatility
        T = input_data.time_horizon
        N = input_data.num_time_steps
        M = input_data.num_paths

        dt = T / N
        time_grid = np.linspace(0, T, N + 1)

        if correlated_shocks is None:
            # Generate standard normal random variables for each time step and path
            correlated_shocks = np.random.standard_normal(size=(N, M))

        # Initialize array to store simulation paths
        paths = np.zeros((N + 1, M))
        paths[0, :] = S0

        for t in range(N):
            # Apply FX GBM step for each path
            paths[t + 1, :] = formulas.fx_gbm_step(paths[t, :], r_d, r_f, sigma, dt, correlated_shocks[t, :])

        return FXGBMSimulationResult(paths=paths, time_grid=time_grid)

    def calibrate(self, *args, **kwargs):
        raise NotImplementedError("FX GBM Model does not require calibration in this context; parameters are direct inputs.")

    def train(self, historical_data):
        raise NotImplementedError("The FX GBM Model is a stochastic model and does not require training.")

    def predict(self, input_features):
        raise NotImplementedError("The FX GBM Model uses 'simulate' for generating future paths, not 'predict'.")
