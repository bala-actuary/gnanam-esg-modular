# Software Design Document (SDD)
### Model Plugin: Merton Model for Credit Risk
**Version:** 1.0
**Date:** 28 June 2025

## 1. Introduction

#### 1.1 Purpose
This document provides the detailed software design for the **Merton Model Plugin**. It is the technical implementation plan for the requirements specified in `Merton_SRS.md` and is designed to conform to the master `PLATFORM_ARCHITECTURE.md`.

#### 1.2 Scope
This design covers the internal structure of the Merton Model plugin, including its primary class, data structures, core algorithms for calibration and calculation of default probability and credit spread, and its data interface with the file system.

## 2. High-Level Design

#### 2.1 Architectural Approach
The plugin will be developed as a self-contained Python package within the `src/models/Credit_Risk/merton_model/` directory. The design will be centered around a main `MertonModel` class. Helper functions for mathematical formulas and calculations will be separated into their own modules for clarity and testability.

#### 2.2 Module Structure
```
/merton_model/
|-- docs/
|   |-- Merton_SRS.md
|   `-- Merton_SDD.md
|
|-- __init__.py
|-- model.py          # Contains the main MertonModel class.
|-- formulas.py       # Contains pure mathematical functions (e.g., Black-Scholes related).
|-- calculations.py   # Contains logic for PD and Credit Spread calculations.
`-- data_structures.py # Defines data classes for inputs and outputs.
```

#### 2.3 Data Interface (File-Based)
To decouple the model logic from data management, the plugin will interact with the file system for its primary inputs and outputs. This allows for easier testing, data versioning, and integration into larger workflows.

*   **Input Directory:** `RiskModels/data/inputs/merton_model/`
    *   `firm_data.csv`: Contains the input data for firm-specific parameters. Columns: `Equity_Value`, `Equity_Volatility`, `Face_Value_Debt`, `Time_to_Maturity`, `Risk_Free_Rate`.
*   **Output Directory:** `RiskModels/data/outputs/merton_model/`
    *   `merton_results.csv`: Stores the primary output of the model (e.g., Implied Asset Value, Implied Asset Volatility, Default Probability, Credit Spread).
    *   `simulated_asset_paths.html`: Interactive HTML plot visualizing simulated asset paths.
    *   `default_probability_over_time.html`: Interactive HTML plot showing default probability over time.


## 3. Detailed Component Design

### 3.1. Data Structures (`data_structures.py`)
We will use Python's `dataclasses` for creating simple, typed data containers.

```python
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
    time_grid: np.ndarray # The time steps used in the simulation
    default_events: np.ndarray # Boolean array indicating default at each step

# Data loading will be handled within the model.py module, which will
# read the CSV files and construct the necessary internal data representations.
```

### 3.2. Mathematical Formulas (`formulas.py`)
This module will contain pure, stateless functions for the core Merton Model mathematical components, primarily related to the Black-Scholes framework.

```python
import numpy as np
from scipy.stats import norm

def d1(S, K, T, r, sigma):
    """Calculates the d1 term of the Black-Scholes formula."""
    pass

def d2(S, K, T, r, sigma):
    """Calculates the d2 term of the Black-Scholes formula."""
    pass

def black_scholes_call(S, K, T, r, sigma):
    """Calculates the Black-Scholes call option price."""
    pass
```

### 3.3. Calculations (`calculations.py`)
This module will house the logic for calculating default probability and credit spread, which depend on the calibrated asset value and volatility.

```python
import numpy as np
from scipy.stats import norm
from .formulas import d2

def calculate_default_probability(asset_value, asset_volatility, face_value_debt, time_to_maturity, risk_free_rate):
    """Calculates the default probability using the Merton Model."""
    pass

def calculate_credit_spread(asset_value, asset_volatility, face_value_debt, time_to_maturity, risk_free_rate):
    """Calculates the credit spread using the Merton Model."""
    pass
```

### 3.4. Main Plugin Class (`model.py`)
This is the public-facing class of the plugin, implementing the `ModelInterface`.

```python
from . import calculations, formulas
from .data_structures import MertonInputData, CalibratedMertonModel, MertonOutputResults
import pandas as pd
import os
from scipy.optimize import fsolve

# Assume ModelInterface is imported from the Core Engine
class MertonModel(ModelInterface):

    def __init__(self, input_dir="RiskModels/data/inputs/merton_model", output_dir="RiskModels/data/outputs/merton_model"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_name(self) -> str:
        return "merton_model"

    def get_required_risk_factors(self) -> list[str]:
        return ["equity_value", "equity_volatility", "face_value_debt", "time_to_maturity", "risk_free_rate"]

    # --- Public Methods (for file-based I/O and convenience) ---

    def calibrate(self) -> CalibratedMertonModel:
        # 1. Load `firm_data.csv` from self.input_dir using pandas.
        # 2. Call the internal logic method to calibrate.
        pass

    def simulate(self, calibrated_model, scenario_definition, correlated_shocks=None):
        # (Future) Implement simulation of asset paths.
        pass

    # --- Internal Logic Methods (for pure in-memory operations) ---

    def _load_and_prepare_data(self) -> MertonInputData:
        # Load data from CSV file
        firm_data_path = os.path.join(self.input_dir, "firm_data.csv")
        df = pd.read_csv(firm_data_path)
        # Assuming single row for now
        return MertonInputData(
            equity_value=df['Equity_Value'].iloc[0],
            equity_volatility=df['Equity_Volatility'].iloc[0],
            face_value_debt=df['Face_Value_Debt'].iloc[0],
            time_to_maturity=df['Time_to_Maturity'].iloc[0],
            risk_free_rate=df['Risk_Free_Rate'].iloc[0]
        )

    def _calibrate_logic(self, input_data: MertonInputData) -> CalibratedMertonModel:
        # Implement the calibration logic to find Asset Value (V_A) and Asset Volatility (sigma_A)
        # This typically involves solving a system of two non-linear equations.
        pass

    def _calculate_results_logic(self, calibrated_model: CalibratedMertonModel, input_data: MertonInputData) -> MertonOutputResults:
        # Calculate PD and Credit Spread using calibrated_model and input_data
        pass

    def train(self, historical_data):
        raise NotImplementedError("The Merton Model is a structural model and does not require training in this context.")

    def predict(self, input_features):
        raise NotImplementedError("The Merton Model uses 'calibrate' and 'calculate_results' for its primary operations, not 'predict'.")
```

### 3.5. Model Fine-Tuning Considerations (HIGH PRIORITY)

This section outlines critical considerations for fine-tuning the Merton Model, particularly concerning input data and output interpretation.

#### 3.5.1. Input Data: Granularity and Consistency

For the `firm_data.csv` input, the consistency and accuracy of the financial data are paramount. We need to discuss and define:

*   **Data Source:** How will we ensure the reliability and timeliness of input data (Equity Value, Equity Volatility, Face Value of Debt, Time to Maturity, Risk-Free Rate)?
*   **Frequency:** What is the expected frequency of input data updates (e.g., daily, weekly, quarterly)?
*   **Consistency:** How will we handle potential inconsistencies or missing data points?

#### 3.5.2. Output Data: Labeling and Format

To enhance usability and interpretability, we need to refine the output format and labeling. This includes:

*   **Column Headers:** Ensure clear and descriptive column headers for `merton_results.csv` (e.g., `Implied_Asset_Value`, `Implied_Asset_Volatility`, `Default_Probability`, `Credit_Spread`).
*   **Units:** Clearly indicate the units for all output metrics (e.g., currency for asset value, percentage for volatility, basis points for credit spread).
*   **Metadata:** Discuss the inclusion of metadata within the output file or a companion file (e.g., input parameters used for the calculation).

#### 3.5.3. Configurable Graphical Output (Future)

Once simulation capabilities are added, the model will support configurable graphical output similar to the HW1F model. This will allow users to select desired plot types (e.g., simulated asset paths, default probability over time) and their configurations as part of the model's run settings.

## 4. Key Algorithms

*   **Calibration:** The calibration of the Merton Model involves solving a system of two non-linear equations to derive the implied asset value and asset volatility from observable equity data. This will likely use a numerical solver such as `scipy.optimize.fsolve`.
*   **Default Probability:** Calculated using the cumulative normal distribution function based on the distance to default.
*   **Credit Spread:** Derived from the default probability and the recovery rate (which may be an input or assumed).

## 5. Dependencies
*   **NumPy:** For all numerical operations.
*   **SciPy:** For optimization (`fsolve`) and statistical functions (`norm`).
*   **Pandas:** For reading and managing the input/output CSV files.

This design provides a clear, modular, and testable structure for the Merton Model plugin that fully aligns with our architectural goals.
