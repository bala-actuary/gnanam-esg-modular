### **Internal User Guide (Draft): Hull-White One-Factor (HW1F) Model**

**Version:** 0.3
**Date:** 28 June 2025
**Purpose:** This document describes how to use the `HullWhiteOneFactor` model plugin, focusing on its dual interface for both file-based and in-memory data operations.

---

### **1. Overview**

The Hull-White One-Factor (HW1F) model is a tool for simulating future interest rate paths. Its primary use is to price interest rate-sensitive instruments and to measure and manage interest rate risk.

Using the model involves three main stages:
1.  **Prepare Input Data:** Place formatted CSV files with market data into the correct input directory (for file-based operations).
2.  **Run Calibration:** Tune the model to reflect the provided market data.
3.  **Run Simulation:** Use the calibrated model to generate future interest rate scenarios, which can be saved to the output directory.

---

### **2. Data Input and Output**

The model offers two primary ways to interact with data:

**A. File-Based I/O (Convenience for Standalone Use)**
For ease of use and to avoid hardcoding, the model can read its inputs from and write its outputs to a standardized directory structure.

*   **Input Directory:** `RiskModels/data/inputs/hull_white_one_factor/`
*   **Output Directory:** `RiskModels/data/outputs/hull_white_one_factor/`

#### **Input File Formats**

The model expects the following CSV files in the input directory:

**a) `initial_zcb_curve.csv`**
*   **Purpose:** Defines the initial yield curve.
*   **Format:** A CSV file with two columns: `Maturity` (in years) and `Price`.
    ```csv
    Maturity,Price
    0.25,0.9980
    0.50,0.9950
    1.00,0.9900
    ...
    ```

**b) `swaption_volatilities.csv`**
*   **Purpose:** Provides market-implied swaption volatilities for calibration.
*   **Format:** A CSV file where the first column is the `Tenor` (in years) and subsequent columns are the swap terms (e.g., `1Y`, `2Y`, etc.).
    ```csv
    Tenor,1Y,2Y,3Y,5Y
    1Y,0.15,0.14,0.135,0.13
    2Y,0.145,0.138,0.132,0.128
    ...
    ```

#### **Output File Format**

The model saves its primary simulation results and generated plots to the output directory.

**a) `simulated_short_rates.csv`**
*   **Purpose:** Stores the generated future short rate scenarios.
*   **Format:** A CSV file where the first column is `Time` (in years) and subsequent columns are `Path_0`, `Path_1`, ..., `Path_N-1` for each simulated path.
    ```csv
    Time,Path_0,Path_1,...
    0.0,0.016,0.016,...
    0.083,0.013,0.012,...
    ...
    ```

**b) `simulated_short_rate_paths.html`**
*   **Purpose:** An interactive HTML plot visualizing individual short rate paths over time.
*   **Format:** An HTML file that can be opened directly in a web browser.

**c) `simulated_short_rate_distribution.html`**
*   **Purpose:** An interactive HTML plot showing the distribution of short rates at selected time points (e.g., 1 year, 3 years, 5 years).
*   **Format:** An HTML file that can be opened directly in a web browser.

**B. In-Memory Data (For Core Engine Integration)**
For direct integration with the Core Engine or other Python modules, the model also exposes internal logic methods that operate directly on in-memory data structures. This avoids file I/O overhead for real-time or programmatic use.

---

### **3. Step 1: Calibrating the Model**

**Goal:** To create a `CalibratedHW1FModel` object that accurately represents the current interest rate environment.

#### **A. Using File-Based Input (Public `calibrate()` method)**

This is done by calling the public `calibrate` method without any arguments. It automatically loads and processes the required data from the CSV files located in the input directory (`RiskModels/data/inputs/hull_white_one_factor/`).

```python
# The model will find and use the CSV files automatically
calibrated_model = hull_white_model.calibrate()
```

The model will internally construct the necessary `initial_zero_coupon_bond_pricer` and `swaptions` data structures from the provided files and then pass them to the internal logic method.

#### **B. Using In-Memory Input (Internal `_calibrate_logic()` method)**

For direct programmatic control, you can call the internal `_calibrate_logic` method, passing the data directly as Python objects:

```python
# Example of in-memory data structures
initial_zcb_pricer_func = lambda t: 1.0 / (1.0 + 0.02 * t) # Example function
market_swaptions_list = [
    {"swap_rate": 0.035, "expiry": 1.0, "tenor_start": 1.0, "tenor_end": 11.0, "fixed_frequency": 0.5, "market_price": 15.25},
    # ... more swaptions
]

calibrated_model = hull_white_model._calibrate_logic(initial_zcb_pricer_func, market_swaptions_list)
```

#### **Output of Calibration**

Both methods return a `CalibratedHW1FModel` object. This object contains the results of the calibration, including:

*   `a`: The calibrated mean-reversion speed.
*   `sigma`: The calibrated volatility parameter.
*   `calibration_error`: A number indicating how closely the model could match the provided market prices. A lower number is better.

You will pass this entire object directly to the simulation step.

---

### **4. Step 2: Simulating Interest Rates**

**Goal:** To generate a set of possible future interest rate paths using the `CalibratedHW1FModel` object from Step 1.

#### **A. Saving to File (Public `simulate()` method)**

This is done by calling the public `simulate` method. It takes the `calibrated_model`, `scenario_definition`, and an optional `plot_options` dictionary as arguments. It will generate random shocks internally if `correlated_shocks` are not provided.

```python
scenario_definition = {
    "num_paths": 5000,
    "time_horizon": 20.0, # 20 years
    "dt": 1/12           # Monthly time steps
}

# Example plot_options to enable only short rate paths plot
plot_options = {
    "short_rate_paths": {"enabled": True, "output_filename": "my_custom_paths.html"},
    "short_rate_distribution": {"enabled": False} # Disable distribution plot
}

simulation_result = hull_white_model.simulate(calibrated_model, scenario_definition, plot_options=plot_options)
```

If `plot_options` is not provided, default plots (short rate paths and distribution) will be generated. You can enable or disable specific plots and customize their output filenames. The method returns an `HW1FSimulationResult` object for immediate in-memory use, and the primary output (`simulated_short_rates.csv`) along with the specified plots are saved to the output directory (`RiskModels/data/outputs/hull_white_one_factor/`).

#### **B. In-Memory Output (Internal `_simulate_logic()` method)**

For direct programmatic control without file I/O, you can call the internal `_simulate_logic` method. This method requires the `calibrated_model`, `scenario_definition`, and `correlated_shocks` (which must be provided, not generated internally).

```python
# Example of generating correlated shocks
num_timesteps = int(scenario_definition["time_horizon"] / scenario_definition["dt"]) + 1
correlated_shocks_array = np.random.standard_normal(size=(num_timesteps - 1, scenario_definition["num_paths"]))

simulation_result = hull_white_model._simulate_logic(calibrated_model, scenario_definition, correlated_shocks_array)
```

This method returns an `HW1FSimulationResult` object directly, without saving any files.

#### **Output of Simulation**

Both methods return an `HW1FSimulationResult` object. This object contains:

*   `paths`: A large table (NumPy array) of the simulated short-rate paths.
*   `time_grid`: A list of the time points corresponding to the rows in the `paths` table.

You can now use this `paths` table for risk analysis, pricing, and other calculations.