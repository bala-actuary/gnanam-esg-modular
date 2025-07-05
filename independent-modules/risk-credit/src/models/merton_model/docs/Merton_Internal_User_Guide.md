### **Internal User Guide (Draft): Merton Model for Credit Risk**

**Version:** 1.0
**Date:** 28 June 2025
**Purpose:** This document describes how to use the `MertonModel` plugin, focusing on its dual interface for both file-based and in-memory data operations.

---

### **1. Overview**

The Merton Model is a structural credit risk model that uses option pricing theory to estimate a firm's probability of default and credit spread. It views a firm's equity as a call option on its assets, with the face value of debt as the strike price.

Using the model involves two main stages:
1.  **Prepare Input Data:** Place formatted CSV files with firm-specific data into the correct input directory (for file-based operations).
2.  **Run Calibration and Calculation:** Calibrate the model to derive implied asset value and volatility, and then calculate the probability of default and credit spread.

---

### **2. Data Input and Output**

The model offers two primary ways to interact with data:

**A. File-Based I/O (Convenience for Standalone Use)**
For ease of use and to avoid hardcoding, the model can read its inputs from and write its outputs to a standardized directory structure.

*   **Input Directory:** `RiskModels/data/inputs/merton_model/`
*   **Output Directory:** `RiskModels/data/outputs/merton_model/`

#### **Input File Formats**

The model expects the following CSV file in the input directory:

**a) `firm_data.csv`**
*   **Purpose:** Defines the input parameters for the Merton Model.
*   **Format:** A CSV file with the following columns:
    *   `Equity_Value`: Current market value of the firm's equity.
    *   `Equity_Volatility`: Volatility of the firm's equity.
    *   `Face_Value_Debt`: Face value of the firm's zero-coupon debt.
    *   `Time_to_Maturity`: Time to maturity of the debt (in years).
    *   `Risk_Free_Rate`: Risk-free interest rate.

    ```csv
    Equity_Value,Equity_Volatility,Face_Value_Debt,Time_to_Maturity,Risk_Free_Rate
    100,0.25,80,1,0.05
    ```

#### **Output File Format**

The model saves its primary results to the output directory.

**a) `merton_results.csv`**
*   **Purpose:** Stores the calculated implied asset value, implied asset volatility, probability of default, and credit spread.
*   **Format:** A CSV file with the following columns:
    *   `Implied_Asset_Value`
    *   `Implied_Asset_Volatility`
    *   `Default_Probability`
    *   `Credit_Spread`

    ```csv
    Implied_Asset_Value,Implied_Asset_Volatility,Default_Probability,Credit_Spread
    150.0,0.30,0.01,50
    ```

**B. In-Memory Data (For Core Engine Integration)**
For direct integration with the Core Engine or other Python modules, the model also exposes internal logic methods that operate directly on in-memory data structures. This avoids file I/O overhead for real-time or programmatic use.

---

### **3. Step 1: Calibrating the Model and Calculating Results**

**Goal:** To calculate the implied asset value and volatility, and subsequently the probability of default and credit spread.

#### **A. Using File-Based Input (Public `calibrate()` and `calculate_results()` methods)**

This is done by calling the public `calibrate` method, which automatically loads and processes the required data from `firm_data.csv`. After calibration, you can call `calculate_results`.

```python
from models.Credit_Risk.merton_model.model import MertonModel

merton_model = MertonModel()

# Calibrate the model (loads data from file and performs calibration)
calibrated_model = merton_model.calibrate()

# Calculate results (PD, Credit Spread) and save to file
merton_model.calculate_results(calibrated_model)
```

#### **B. Using In-Memory Input (Internal `_calibrate_logic()` and `_calculate_results_logic()` methods)**

For direct programmatic control, you can call the internal `_calibrate_logic` and `_calculate_results_logic` methods, passing the data directly as Python objects:

```python
from models.Credit_Risk.merton_model.model import MertonModel
from models.Credit_Risk.merton_model.data_structures import MertonInputData

merton_model = MertonModel()

# Example of in-memory input data
input_data = MertonInputData(
    equity_value=100.0,
    equity_volatility=0.25,
    face_value_debt=80.0,
    time_to_maturity=1.0,
    risk_free_rate=0.05
)

# Calibrate the model with in-memory data
calibrated_model = merton_model._calibrate_logic(input_data)

# Calculate results with in-memory data
results = merton_model._calculate_results_logic(calibrated_model, input_data)

print(f"Default Probability: {results.default_probability}")
print(f"Credit Spread: {results.credit_spread}")
```

#### **Output of Calibration and Calculation**

*   `calibrate()` returns a `CalibratedMertonModel` object containing `asset_value` and `asset_volatility`.
*   `calculate_results()` (public) saves `merton_results.csv` and returns `MertonOutputResults`.
*   `_calculate_results_logic()` (internal) returns a `MertonOutputResults` object directly.

---

### **4. Simulating Asset Values and Default Paths**

**Goal:** To generate future asset value paths and identify default events over time.

#### **A. Using File-Based Input (Public `simulate()` method)**

This is done by calling the public `simulate` method, which takes a `CalibratedMertonModel` object (obtained from `calibrate()`) and a `scenario_definition` dictionary. It will automatically save simulated paths to a CSV file and generate interactive HTML plots.

```python
from models.Credit_Risk.merton_model.model import MertonModel

merton_model = MertonModel()

# Calibrate the model first
calibrated_model = merton_model.calibrate()

# Define scenario definition for simulation
scenario_definition = {
    'time_horizon': 1.0,
    'num_time_steps': 252,
    'num_paths': 100
}

# Define plot options (optional)
plot_options = {
    "asset_paths": {"enabled": True, "output_filename": "simulated_asset_paths.html"},
    "default_probability_over_time": {"enabled": True, "output_filename": "default_probability_over_time.html"}
}

# Simulate the model
simulation_result = merton_model.simulate(calibrated_model, scenario_definition, plot_options=plot_options)

print(f"Simulation output saved to: {merton_model.output_dir}/simulated_asset_paths.csv")
print(f"Plots saved to: {merton_model.output_dir}/simulated_asset_paths.html and {merton_model.output_dir}/default_probability_over_time.html")
```

#### **B. Using In-Memory Input (Internal `_simulate_logic()` method)**

For direct programmatic control, you can call the internal `_simulate_logic` method, passing the data directly as Python objects:

```python
from models.Credit_Risk.merton_model.model import MertonModel
from models.Credit_Risk.merton_model.data_structures import CalibratedMertonModel
import numpy as np

merton_model = MertonModel()

# Assume you have a calibrated_model object and scenario_definition
# For example, from a previous calibration:
calibrated_model = CalibratedMertonModel(asset_value=150.0, asset_volatility=0.25)

scenario_definition = {
    'time_horizon': 1.0,
    'num_time_steps': 252,
    'num_paths': 10
}

# Generate correlated shocks (e.g., standard normal random variables)
num_timesteps = int(scenario_definition['time_horizon'] / (scenario_definition['time_horizon'] / scenario_definition['num_time_steps'])) + 1
correlated_shocks = np.random.standard_normal(size=(num_timesteps - 1, scenario_definition['num_paths']))

simulation_result = merton_model._simulate_logic(calibrated_model, scenario_definition, correlated_shocks)

print(f"Simulated paths shape: {simulation_result.paths.shape}")
```

#### **Output of Simulation**

*   `simulate()` returns a `MertonSimulationResult` object containing `paths` (simulated asset values), `time_grid`, and `default_events` (boolean array indicating default at each step).
*   The public `simulate()` method also saves `simulated_asset_paths.csv` and generates `simulated_asset_paths.html` and `default_probability_over_time.html`.

---

### **5. Using the API Endpoint (Recommended for Most Users)**

With the new RiskModels API, you can run the Merton model securely and easily from your browser or any tool that can make web requests. This is the recommended way for most users, especially non-programmers.

#### **A. How to Use the API**

1. **Log in to the API** using your username and password to get your access token.
2. **Go to the API documentation page:**
   - Open your browser and visit: `http://127.0.0.1:8000/docs`
   - This page lets you try out the Merton model interactively.
3. **Find the `/api/run/merton_model` endpoint.**
4. **Fill in the scenario parameters** (number of paths, time steps, time horizon, etc.).
   - You can use the default values or enter your own.
5. **Authorize with your token** (click "Authorize" in the docs UI and paste your token).
6. **Click "Execute"** to run the simulation.
7. **View or download the results** (returned as JSON for easy use in Excel, Python, R, etc.).

#### **B. Where to Find More Help**
- See the [API Quick Start Guide](../../../../docs/guides/quickstart_api.md) for a plain-English walkthrough and more details.
- The API is secure: only authenticated users can run models.

#### **C. Why Use the API?**
- No coding required—just fill in a form and get results.
- Works for both technical and non-technical users.
- Results are returned instantly and can be used in any analysis tool.

**In summary:**
You can now run the Merton model from your browser, securely and easily, without writing any code. For advanced use, you can still use the Python interfaces described above.
