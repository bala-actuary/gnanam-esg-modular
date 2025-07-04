# Software Design Document (SDD)
### Model Plugin: Basic Exposure Model for Counterparty Risk
**Version:** 1.0
**Date:** 28 June 2025

## 1. Introduction

#### 1.1 Purpose
This document provides the detailed software design for the **Basic Exposure Model Plugin**. It is the technical implementation plan for the requirements specified in `Basic_Exposure_SRS.md` and is designed to conform to the master `PLATFORM_ARCHITECTURE.md`.

#### 1.2 Scope
This design covers the internal structure of the Basic Exposure Model plugin, including its primary class, data structures, core algorithms for exposure calculation, and its data interface with the file system.

## 2. High-Level Design

#### 2.1 Architectural Approach
The plugin will be developed as a self-contained Python package within the `src/models/Counterparty_Risk/basic_exposure_model/` directory. The design will be centered around a main `BasicExposureModel` class. Helper functions for calculations will be separated into their own modules for clarity and testability.

#### 2.2 Module Structure
```
/basic_exposure_model/
|-- docs/
|   |-- Basic_Exposure_SRS.md
|   `-- Basic_Exposure_SDD.md
|
|-- __init__.py
|-- model.py          # Contains the main BasicExposureModel class.
|-- calculations.py   # Contains logic for exposure calculations.
`-- data_structures.py # Defines data classes for inputs and outputs.
```

#### 2.3 Data Interface (File-Based)
To decouple the model logic from data management, the plugin will interact with the file system for its primary inputs and outputs. This allows for easier testing, data versioning, and integration into larger workflows.

*   **Input Directory:** `RiskModels/data/inputs/counterparty_risk/`
    *   `trades_portfolio.csv`: Contains the input data for trades. Columns: `Counterparty_ID`, `Trade_ID`, `Market_Value`.
*   **Output Directory:** `RiskModels/data/outputs/counterparty_risk/`
    *   `exposure_results.csv`: Stores the primary output of the model (total, positive, and negative exposure per counterparty).
    *   `exposure_plot.html`: Interactive HTML plot visualizing exposures per counterparty.


## 3. Detailed Component Design

### 3.1. Data Structures (`data_structures.py`)
We will use Python's `dataclasses` for creating simple, typed data containers.

```python
from dataclasses import dataclass
import pandas as pd

@dataclass
class TradePortfolioInputData:
    """Data container for the input trade portfolio data."""
    portfolio_df: pd.DataFrame # DataFrame with Counterparty_ID, Trade_ID, Market_Value

@dataclass
class ExposureResults:
    """Data container for the calculated exposure results."""
    results_df: pd.DataFrame # DataFrame with Counterparty_ID, Total_Exposure, Positive_Exposure, Negative_Exposure

# Data loading will be handled within the model.py module, which will
# read the CSV files and construct the necessary internal data representations.
```

### 3.2. Calculations (`calculations.py`)
This module will contain pure, stateless functions for exposure calculations.

```python
import pandas as pd

def calculate_counterparty_exposures(portfolio_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates total, positive, and negative exposures per counterparty."""
    pass
```

### 3.3. Main Plugin Class (`model.py`)
This is the public-facing class of the plugin, implementing the `ModelInterface`.

```python
from . import calculations
from .data_structures import TradePortfolioInputData, ExposureResults
import pandas as pd
import os

# Assume ModelInterface is imported from the Core Engine
class BasicExposureModel(ModelInterface):

    def __init__(self, input_dir="RiskModels/data/inputs/counterparty_risk", output_dir="RiskModels/data/outputs/counterparty_risk"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_name(self) -> str:
        return "basic_exposure_model"

    def get_required_risk_factors(self) -> list[str]:
        return ["trades_portfolio"]

    # --- Public Methods (for file-based I/O and convenience) ---

    def calculate(self, scenario_definition: dict = None, plot_options: dict = None) -> ExposureResults:
        input_data = self._load_and_prepare_data() # scenario_definition can be used for filtering/transforming data
        results = self._calculate_logic(input_data)

        # Save results to CSV
        output_path_csv = os.path.join(self.output_dir, "exposure_results.csv")
        results.results_df.to_csv(output_path_csv, index=False)

        # Generate and save plots based on plot_options
        if plot_options is None:
            plot_options = {
                "exposure_plot": {"enabled": True}
            }

        from visualization.plotter import plot_counterparty_exposures

        if plot_options.get("exposure_plot", {}).get("enabled", False):
            output_filename = plot_options["exposure_plot"].get("output_filename", "exposure_plot.html")
            plot_counterparty_exposures(
                results.results_df,
                os.path.join(self.output_dir, output_filename)
            )

        return results

    # --- Internal Logic Methods (for pure in-memory operations) ---

    def _load_and_prepare_data(self) -> TradePortfolioInputData:
        portfolio_path = os.path.join(self.input_dir, "trades_portfolio.csv")
        df = pd.read_csv(portfolio_path)
        return TradePortfolioInputData(portfolio_df=df)

    def _calculate_logic(self, input_data: TradePortfolioInputData) -> ExposureResults:
        df = input_data.portfolio_df.copy()
        exposure_df = calculations.calculate_counterparty_exposures(df)
        return ExposureResults(results_df=exposure_df)

    def calibrate(self, *args, **kwargs):
        raise NotImplementedError("Basic Exposure Model does not require calibration.")

    def simulate(self, *args, **kwargs):
        raise NotImplementedError("Basic Exposure Model performs calculations, not simulations.")

    def train(self, historical_data):
        raise NotImplementedError("The Basic Exposure Model is a deterministic model and does not require training.")

    def predict(self, input_features):
        raise NotImplementedError("The Basic Exposure Model uses 'calculate' for its primary operations, not 'predict'.")
