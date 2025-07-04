# Software Design Document (SDD)
### Model Plugin: Hull-White One-Factor (HW1F)
**Version:** 1.1
**Date:** 28 June 2025

## 1. Introduction

#### 1.1 Purpose
This document provides the detailed software design for the **Hull-White One-Factor (HW1F) Model Plugin**. It is the technical implementation plan for the requirements specified in `HW1F_SRS.md` and is designed to conform to the master `PLATFORM_ARCHITECTURE.md`.

#### 1.2 Scope
This design covers the internal structure of the HW1F plugin, including its primary class, data structures, core algorithms, and its data interface with the file system.

## 2. High-Level Design

#### 2.1 Architectural Approach
The plugin will be developed as a self-contained Python package within the `src/models/Interest_Rate_Risk/hull_white_one_factor/` directory. The design will be centered around a main `HullWhiteOneFactor` class. Helper functions for complex mathematical formulas and pricing logic will be separated into their own modules for clarity and testability.

#### 2.2 Module Structure
```
/hull_white_one_factor/
|-- docs/
|   |-- HW1F_SRS.md
|   `-- HW1F_SDD.md
|
|-- __init__.py
|-- model.py          # Contains the main HullWhiteOneFactor class.
|-- formulas.py       # Contains pure mathematical functions (A(t,T), B(t,T), etc.).
|-- pricing.py        # Contains derivative pricing logic (ZCBs, Swaptions).
`-- data_structures.py # Defines data classes for inputs and outputs.
```

#### 2.3 Data Interface (File-Based)
To decouple the model logic from data management, the plugin will interact with the file system for its primary inputs and outputs. This allows for easier testing, data versioning, and integration into larger workflows.

*   **Input Directory:** `RiskModels/data/inputs/hull_white_one_factor/`
    *   `initial_zcb_curve.csv`: Contains the initial Zero-Coupon Bond curve. Columns: `Maturity`, `Price`.
    *   `swaption_volatilities.csv`: Contains the market swaption volatility surface. Format: Matrix with `Tenor` as rows and swap terms as columns.
*   **Output Directory:** `RiskModels/data/outputs/hull_white_one_factor/`
    *   `simulated_short_rates.csv`: Stores the primary output of the simulation, containing simulated short rates for each path over time. Columns: `Time`, `Path_0`, `Path_1`, ..., `Path_N-1`.
    *   `simulated_short_rate_paths.html`: Interactive HTML plot visualizing individual short rate paths.
    *   `simulated_short_rate_distribution.html`: Interactive HTML plot showing the distribution of short rates at selected time points.


## 3. Detailed Component Design

### 3.1. Data Structures (`data_structures.py`)
We will use Python's `dataclasses` for creating simple, typed data containers.

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class CalibratedHW1FModel:
    """Data container for the results of a successful calibration."""
    a: float  # Mean reversion speed
    sigma: float  # Volatility
    theta_function: callable  # The determined theta function
    calibration_error: float

@dataclass
class HW1FSimulationResult:
    """Data container for the results of a simulation."""
    paths: np.ndarray  # Shape: (num_timesteps, num_paths)
    time_grid: np.ndarray # The time steps used in the simulation

# Data loading will be handled within the model.py module, which will
# read the CSV files and construct the necessary internal data representations
# (e.g., interpolated curve functions, lists of swaption objects).
```

### 3.2. Mathematical Formulas (`formulas.py`)
This module will contain pure, stateless functions for the core HW1F mathematical components. This allows them to be unit-tested in isolation.

```python
import numpy as np

def B(t: float, T: float, a: float) -> float:
    """Calculates the B(t,T) term of the HW1F model."""
    # Implementation of (1/a) * (1 - exp(-a(T-t)))
    pass

def A(t: float, T: float, calibrated_model: CalibratedHW1FModel) -> float:
    """Calculates the A(t,T) term of the HW1F model."""
    # This will require access to the initial market curve data
    # passed within a larger data bundle.
    pass
```

### 3.3. Derivative Pricing (`pricing.py`)
This module will house the logic for pricing derivatives, which is required during the calibration process.

```python
from . import formulas
from .data_structures import CalibratedHW1FModel

def price_zcb(t: float, T: float, r_t: float, calibrated_model: CalibratedHW1FModel) -> float:
    """Prices a Zero-Coupon Bond using the analytical formula."""
    # P(t,T) = A(t,T) * exp(-B(t,T) * r_t)
    pass

def price_european_swaption(...):
    """Prices a European swaption using Jamshidian's Trick."""
    # This will be a complex function involving:
    # 1. Defining the swap's cash flows as a series of ZCBs.
    # 2. Finding the critical rate r* that makes the swap value zero at expiry.
    # 3. Decomposing the swaption into a portfolio of options on ZCBs.
    # 4. Pricing each ZCB option using the appropriate Black-like formula.
    pass
```

### 3.4. Main Plugin Class (`model.py`)
This is the public-facing class of the plugin, implementing the `ModelInterface`.

```python
from . import pricing, formulas
from .data_structures import CalibratedHW1FModel, HW1FSimulationResult
from scipy.optimize import minimize
import pandas as pd # For data loading
import os

# Assume ModelInterface is imported from the Core Engine
class HullWhiteOneFactor(ModelInterface):

    def __init__(self, input_dir="RiskModels/data/inputs/hull_white_one_factor", output_dir="RiskModels/data/outputs/hull_white_one_factor"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_name(self) -> str:
        return "hull_white_one_factor"

    # --- Public Methods (for file-based I/O and convenience) ---

    def calibrate(self) -> CalibratedHW1FModel:
        # 1. Load `initial_zcb_curve.csv` and `swaption_volatilities.csv`
        #    from self.input_dir using pandas.
        # 2. Construct internal data representations (e.g., an interpolated
        #    yield curve function and a list of swaption objects).
        initial_zero_coupon_bond_pricer, market_swaptions = self._load_and_prepare_data()
        # 3. Call the internal logic method
        return self._calibrate_logic(initial_zero_coupon_bond_pricer, market_swaptions)

    def simulate(self, calibrated_model: CalibratedHW1FModel, scenario_definition, correlated_shocks=None) -> HW1FSimulationResult:
        # 1. Generate random shocks internally if not provided.
        num_paths = scenario_definition['num_paths']
        time_horizon = scenario_definition['time_horizon']
        dt = scenario_definition['dt']
        num_timesteps = int(time_horizon / dt) + 1

        if correlated_shocks is None:
            correlated_shocks = np.random.standard_normal(size=(num_timesteps - 1, num_paths))

        # 2. Call the internal logic method
        simulation_result = self._simulate_logic(calibrated_model, scenario_definition, correlated_shocks)

        # 3. Save results to CSV
        output_path = os.path.join(self.output_dir, "simulated_yield_curves.csv")
        # A more detailed implementation would convert short rates to yield curves before saving
        pd.DataFrame(simulation_result.paths, index=simulation_result.time_grid).to_csv(output_path)

        return simulation_result

    # --- Internal Logic Methods (for pure in-memory operations) ---

    def _load_and_prepare_data(self):
        # Load data from CSV files
        zcb_curve_path = os.path.join(self.input_dir, "initial_zcb_curve.csv")
        swaptions_path = os.path.join(self.input_dir, "swaption_volatilities.csv")

        zcb_df = pd.read_csv(zcb_curve_path)
        swaptions_df = pd.read_csv(swaptions_path)

        # Create an interpolated pricer function from the ZCB curve data
        initial_zero_coupon_bond_pricer = interp1d(
            zcb_df['Maturity'], zcb_df['Price'],
            kind='cubic', fill_value="extrapolate"
        )

        # Convert swaption volatility dataframe to a list of dicts for calibration
        # This part needs a more robust implementation based on how swaption details are provided.
        # For now, we assume a simplified structure.
        market_swaptions = [] # This would be built from swaptions_df

        return initial_zero_coupon_bond_pricer, market_swaptions

    def _calibrate_logic(self, initial_zero_coupon_bond_pricer, market_swaptions) -> CalibratedHW1FModel:
        # Original calibration logic here, operating on in-memory data
        def objective_function(params):
            a, sigma = params
            if a <= 0 or sigma <= 0: # Ensure positive parameters
                return np.inf

            # Generate theta function for current a, sigma
            theta_func = formulas.generate_theta_function(a, sigma, initial_zero_coupon_bond_pricer)

            # Create a temporary calibrated model for pricing
            temp_calibrated_model = CalibratedHW1FModel(
                a=a, sigma=sigma, theta_function=theta_func,
                calibration_error=0.0, # Placeholder
                initial_zero_coupon_bond_pricer=initial_zero_coupon_bond_pricer
            )

            total_error = 0.0
            for swaption in market_swaptions:
                model_price = pricing.price_european_swaption(
                    swap_rate=swaption['swap_rate'],
                    expiry=swaption['expiry'],
                    tenor_start=swaption['tenor_start'],
                    tenor_end=swaption['tenor_end'],
                    fixed_frequency=swaption['fixed_frequency'],
                    calibrated_model=temp_calibrated_model,
                    option_type=swaption.get('option_type', 'payer') # Default to payer
                )
                total_error += (model_price - swaption['market_price'])**2
            return total_error

        # Initial guess for a and sigma (can be refined)
        initial_guess = [0.1, 0.01] # Example values
        bounds = ((1e-5, None), (1e-5, None)) # a > 0, sigma > 0

        result = minimize(objective_function, initial_guess, method='L-BFGS-B', bounds=bounds)

        if not result.success:
            raise RuntimeError(f"Calibration failed: {result.message}")

        calibrated_a, calibrated_sigma = result.x
        final_theta_func = formulas.generate_theta_function(calibrated_a, calibrated_sigma, initial_zero_coupon_bond_pricer)

        return CalibratedHW1FModel(
            a=calibrated_a,
            sigma=calibrated_sigma,
            theta_function=final_theta_func,
            calibration_error=result.fun,
            initial_zero_coupon_bond_pricer=initial_zero_coupon_bond_pricer
        )

    def _simulate_logic(self, calibrated_model: CalibratedHW1FModel, scenario_definition, correlated_shocks) -> HW1FSimulationResult:
        # Original simulation logic here, operating on in-memory data
        a = calibrated_model.a
        sigma = calibrated_model.sigma
        theta_function = calibrated_model.theta_function
        initial_zero_coupon_bond_pricer = calibrated_model.initial_zero_coupon_bond_pricer

        num_paths = scenario_definition['num_paths']
        time_horizon = scenario_definition['time_horizon']
        dt = scenario_definition['dt']

        num_timesteps = int(time_horizon / dt) + 1
        time_grid = np.linspace(0, time_horizon, num_timesteps)

        # Get initial short rate r(0) from the initial curve
        # f(0,0) is not well-defined, so we use f(0, epsilon) as an approximation for r(0)
        epsilon = 1e-5
        r0 = formulas.instantaneous_forward_rate(epsilon, initial_zero_coupon_bond_pricer)

        paths = np.zeros((num_timesteps, num_paths))
        paths[0, :] = r0

        for i in range(num_timesteps - 1):
            t = time_grid[i]
            r_t = paths[i, :]
            dW_t = correlated_shocks[i, :]

            drift = (theta_function(t) - a * r_t) * dt
            stochastic = sigma * np.sqrt(dt) * dW_t

            paths[i+1, :] = r_t + drift + stochastic

        return HW1FSimulationResult(paths=paths, time_grid=time_grid)

    def get_required_risk_factors(self) -> list[str]:
        return ["risk_free_rate_curve", "swaption_volatility_surface"]

    def train(self, historical_data):
        raise NotImplementedError("The Hull-White One-Factor model is a traditional stochastic model and does not require training.")

    def predict(self, input_features):
        raise NotImplementedError("The Hull-White One-Factor model uses 'simulate' for generating future paths, not 'predict'.")
```

### 3.5. Model Fine-Tuning Considerations (HIGH PRIORITY)

This section outlines critical considerations for fine-tuning the HW1F model, particularly concerning input data granularity and output file formatting.

#### 3.5.1. Input Data: Maturity Period Granularity

For the `initial_zcb_curve.csv` input, the number and distribution of maturity periods are crucial for accurate calibration and simulation. A sufficient number of data points across the relevant maturity spectrum is required to accurately interpolate the initial zero-coupon bond curve. We need to discuss and define:

*   **Minimum number of maturity points:** What is the absolute minimum required for a stable interpolation?
*   **Distribution of maturity points:** Should they be evenly spaced, or concentrated at short, medium, and long ends of the curve?
*   **Standard maturity points:** Are there industry-standard maturity points (e.g., 3M, 6M, 1Y, 2Y, 5Y, 10Y, 20Y, 30Y) that we should aim to support or require?
*   **Impact on interpolation:** How does the choice of maturity points affect the accuracy and stability of the `interp1d` function used for the initial curve?

#### 3.5.2. Output Data: Labeling and Format

The `simulated_yield_curves.csv` output currently contains raw short rates. To enhance usability and interpretability, we need to refine its format and labeling. This includes:

*   **Column Headers:** Ensure clear and descriptive column headers (e.g., `Time`, `Path_1_Rate`, `Path_2_Rate`, etc., or a more structured format if yield curves are output).
*   **Time Representation:** Clearly indicate whether the time column represents years, months, or another unit.
*   **Yield Curve Output:** Instead of just short rates, consider outputting full yield curves at each time step for each path. This would involve converting the simulated short rates into zero-coupon bond prices or par rates, and then into yield curves.
*   **Metadata:** Discuss the inclusion of metadata within the output file or a companion file (e.g., simulation parameters like `num_paths`, `time_horizon`, `dt`, calibration parameters `a`, `sigma`).

#### 3.5.3. Configurable Graphical Output

To provide users with flexibility in visualizing simulation results, the `simulate` method will accept a `plot_options` parameter. This parameter will be a dictionary allowing users to specify which types of plots to generate and their configurations.

Example `plot_options` structure:
```python
plot_options = {
    "short_rate_paths": {
        "enabled": True,
        "output_filename": "custom_short_rate_paths.html"
    },
    "short_rate_distribution": {
        "enabled": True,
        "time_points": [1.0, 2.0, 5.0], # Specific time points for distribution plots
        "output_filename": "custom_short_rate_distribution.html"
    },
    # Future plot types can be added here
}
```
If `plot_options` is not provided or is empty, default plots will be generated. If `enabled` is `False` for a specific plot type, that plot will be skipped. This allows users to control the output based on their analytical needs.

## 4. Key Algorithms

*   **Calibration:** The core algorithm is the minimization of the error function. We will use the **L-BFGS-B** algorithm from `scipy.optimize.minimize` as it is efficient and allows for bounds on the parameters (`a > 0`, `σ > 0`).
*   **Swaption Pricing:** The implementation will strictly follow the methodology of **Jamshidian's Trick (1989)**.
*   **Simulation:** The default simulation will use the **Euler-Maruyama discretization scheme**.

## 5. Dependencies
*   **NumPy:** For all numerical operations.
*   **SciPy:** For optimization (`minimize`) and statistics (`norm`).
*   **Pandas:** For reading and managing the input/output CSV files.

This design provides a clear, modular, and testable structure for the HW1F plugin that fully aligns with our architectural goals.
