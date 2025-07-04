### **Internal User Guide (Draft): Geometric Brownian Motion (GBM) Model**

**Version:** 1.0
**Date:** 28 June 2025
**Purpose:** This document describes how to use the `GBMModel` plugin, focusing on its dual interface for both file-based and in-memory data operations.

---

### **1. Overview**

The Geometric Brownian Motion (GBM) model is a continuous-time stochastic process used to model the random walk of asset prices (e.g., stocks, commodities, currencies). It assumes that the logarithm of the asset price follows a Brownian motion with drift.

Using the model primarily involves:
1.  **Prepare Input Data:** Provide parameters for the GBM process, either through a CSV file or directly in memory.
2.  **Run Simulation:** Generate future asset price paths based on the provided parameters.

---

### **2. Data Input and Output**

The model offers two primary ways to interact with data:

**A. File-Based I/O (Convenience for Standalone Use)**
For ease of use and to avoid hardcoding, the model can read its inputs from and write its outputs to a standardized directory structure.

*   **Input Directory:** `RiskModels/data/inputs/gbm_model/`
*   **Output Directory:** `RiskModels/data/outputs/gbm_model/`

#### **Input File Formats**

The model expects the following CSV file in the input directory:

**a) `gbm_parameters.csv`**
*   **Purpose:** Defines the input parameters for the GBM simulation.
*   **Format:** A CSV file with a single row and the following columns:
    *   `Initial_Price`: The starting price of the asset (S0).
    *   `Expected_Return`: The annualized expected return (mu).
    *   `Volatility`: The annualized volatility (sigma).
    *   `Time_Horizon`: The total time period for the simulation (T, in years).
    *   `Num_Time_Steps`: The number of discrete time steps within the time horizon (N).
    *   `Num_Paths`: The number of simulation paths to generate (M).

    ```csv
    Initial_Price,Expected_Return,Volatility,Time_Horizon,Num_Time_Steps,Num_Paths
    100,0.10,0.20,1,252,1000
    ```

#### **Output File Format**

The model saves its primary simulation results and generated plots to the output directory.

**a) `simulated_prices.csv`**
*   **Purpose:** Stores the generated future asset price paths.
*   **Format:** A CSV file where the first column is `Time` (in years) and subsequent columns are `Path_0`, `Path_1`, ..., `Path_M-1` for each simulated path.
    ```csv
    Time,Path_0,Path_1,...
    0.0,100.0,100.0,...
    0.003968,100.12,99.87,...
    ...
    ```

**b) `simulated_price_paths.html`**
*   **Purpose:** An interactive HTML plot visualizing individual asset price paths over time.
*   **Format:** An HTML file that can be opened directly in a web browser.

**c) `price_distribution_at_maturity.html`**
*   **Purpose:** An interactive HTML plot showing the distribution of asset prices at the end of the simulation horizon.
*   **Format:** An HTML file that can be opened directly in a web browser.

**B. In-Memory Data (For Core Engine Integration)**
For direct integration with the Core Engine or other Python modules, the model also exposes internal logic methods that operate directly on in-memory data structures. This avoids file I/O overhead for real-time or programmatic use.

---

### **3. Step 1: Simulating Asset Prices**

**Goal:** To generate a set of possible future asset price paths.

#### **A. Using File-Based Input (Public `simulate()` method)**

This is done by calling the public `simulate` method. It takes a `scenario_definition` dictionary as an argument, which can override parameters loaded from `gbm_parameters.csv`. It will generate random shocks internally if `correlated_shocks` are not provided.

```python
from models.Equity_Risk.gbm_model.model import GBMModel

gbm_model = GBMModel()

scenario_definition = {
    "initial_price": 100.0,
    "expected_return": 0.10,
    "volatility": 0.20,
    "time_horizon": 1.0,      # 1 year
    "num_time_steps": 252,    # Daily steps for 1 year
    "num_paths": 1000
}

# Example plot_options to enable only price paths plot
plot_options = {
    "price_paths": {"enabled": True, "output_filename": "my_custom_gbm_paths.html"},
    "price_distribution_at_maturity": {"enabled": False} # Disable distribution plot
}

simulation_result = gbm_model.simulate(scenario_definition, plot_options=plot_options)
```

If `plot_options` is not provided, default plots (price paths and distribution) will be generated. You can enable or disable specific plots and customize their output filenames. The method returns a `GBMSimulationResult` object for immediate in-memory use, and the primary output (`simulated_prices.csv`) along with the specified plots are saved to the output directory (`RiskModels/data/outputs/gbm_model/`).

#### **B. In-Memory Output (Internal `_simulate_logic()` method)**

For direct programmatic control without file I/O, you can call the internal `_simulate_logic` method. This method requires a `GBMInputData` object and `correlated_shocks` (which must be provided, not generated internally).

```python
from models.Equity_Risk.gbm_model.model import GBMModel
from models.Equity_Risk.gbm_model.data_structures import GBMInputData

gbm_model = GBMModel()

input_data = GBMInputData(
    initial_price=100.0,
    expected_return=0.10,
    volatility=0.20,
    time_horizon=1.0,
    num_time_steps=252,
    num_paths=1000
)

# Example of generating correlated shocks
num_timesteps = input_data.num_time_steps
num_paths = input_data.num_paths
correlated_shocks_array = np.random.standard_normal(size=(num_timesteps, num_paths))

simulation_result = gbm_model._simulate_logic(input_data, correlated_shocks_array)
```

This method returns a `GBMSimulationResult` object directly, without saving any files.

#### **Output of Simulation**

Both methods return a `GBMSimulationResult` object. This object contains:

*   `paths`: A large table (NumPy array) of the simulated asset price paths.
*   `time_grid`: A list of the time points corresponding to the rows in the `paths` table.

You can now use this `paths` table for further analysis, pricing, and other calculations.

---

### **4. Using the API Endpoint (Recommended for Most Users)**

With the new RiskModels API, you can run the GBM model securely and easily from your browser or any tool that can make web requests. This is the recommended way for most users, especially non-programmers.

#### **A. How to Use the API**

1. **Log in to the API** using your username and password to get your access token.
2. **Go to the API documentation page:**
   - Open your browser and visit: `http://127.0.0.1:8000/docs`
   - This page lets you try out the GBM model interactively.
3. **Find the `/api/run/gbm_model` endpoint.**
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
You can now run the GBM model from your browser, securely and easily, without writing any code. For advanced use, you can still use the Python interfaces described above.
