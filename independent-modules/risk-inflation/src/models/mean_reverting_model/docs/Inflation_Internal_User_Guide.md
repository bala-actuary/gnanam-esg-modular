### **Internal User Guide (Draft): Mean-Reverting Inflation Model**

**Version:** 1.0
**Date:** 28 June 2025
**Purpose:** This document describes how to use the `MeanRevertingInflationModel` plugin, focusing on its dual interface for both file-based and in-memory data operations.

---

### **1. Overview**

The Mean-Reverting Inflation Model is a stochastic process used to simulate future inflation rates. It assumes that inflation rates tend to revert to a long-term average, making it more realistic for modeling inflation than a simple random walk.

Using the model primarily involves:
1.  **Prepare Input Data:** Provide parameters for the mean-reverting process, either through a CSV file or directly in memory.
2.  **Run Simulation:** Generate future inflation rate paths based on the provided parameters.

---

### **2. Data Input and Output**

The model offers two primary ways to interact with data:

**A. File-Based I/O (Convenience for Standalone Use)**
For ease of use and to avoid hardcoding, the model can read its inputs from and write its outputs to a standardized directory structure.

*   **Input Directory:** `RiskModels/data/inputs/inflation_model/`
*   **Output Directory:** `RiskModels/data/outputs/inflation_model/`

#### **Input File Formats**

The model expects the following CSV file in the input directory:

**a) `inflation_parameters.csv`**
*   **Purpose:** Defines the input parameters for the inflation simulation.
*   **Format:** A CSV file with a single row and the following columns:
    *   `Initial_Inflation_Rate`: The starting inflation rate (I0).
    *   `Long_Term_Mean_Inflation_Rate`: The long-term average inflation rate (theta).
    *   `Mean_Reversion_Speed`: The speed at which the inflation rate reverts to the mean (kappa).
    *   `Volatility`: The annualized volatility (sigma).
    *   `Time_Horizon`: The total time period for the simulation (T, in years).
    *   `Num_Time_Steps`: The number of discrete time steps within the time horizon (N).
    *   `Num_Paths`: The number of simulation paths to generate (M).

    ```csv
    Initial_Inflation_Rate,Long_Term_Mean_Inflation_Rate,Mean_Reversion_Speed,Volatility,Time_Horizon,Num_Time_Steps,Num_Paths
    0.02,0.03,0.5,0.01,1,252,1000
    ```

#### **Output File Format**

The model saves its primary simulation results and generated plots to the output directory.

**a) `simulated_inflation_rates.csv`**
*   **Purpose:** Stores the generated future inflation rate paths.
*   **Format:** A CSV file where the first column is `Time` (in years) and subsequent columns are `Path_0`, `Path_1`, ..., `Path_M-1` for each simulated path.
    ```csv
    Time,Path_0,Path_1,...
    0.0,0.02,0.02,...
    0.003968,0.0201,0.0198,...
    ...
    ```

**b) `simulated_inflation_rate_paths.html`**
*   **Purpose:** An interactive HTML plot visualizing individual inflation rate paths over time.
*   **Format:** An HTML file that can be opened directly in a web browser.

**c) `inflation_rate_distribution_at_maturity.html`**
*   **Purpose:** An interactive HTML plot showing the distribution of inflation rates at the end of the simulation horizon.
*   **Format:** An HTML file that can be opened directly in a web browser.

**B. In-Memory Data (For Core Engine Integration)**
For direct integration with the Core Engine or other Python modules, the model also exposes internal logic methods that operate directly on in-memory data structures. This avoids file I/O overhead for real-time or programmatic use.

---

### **3. Step 1: Simulating Inflation Rates**

**Goal:** To generate a set of possible future inflation rate paths.

#### **A. Using File-Based Input (Public `simulate()` method)**

This is done by calling the public `simulate` method. It takes a `scenario_definition` dictionary as an argument, which can override parameters loaded from `inflation_parameters.csv`. It will generate random shocks internally if `correlated_shocks` are not provided.

```python
from models.Inflation_Risk.mean_reverting_model.model import MeanRevertingInflationModel

inflation_model = MeanRevertingInflationModel()

scenario_definition = {
    "initial_inflation_rate": 0.02,
    "long_term_mean_inflation_rate": 0.03,
    "mean_reversion_speed": 0.5,
    "volatility": 0.01,
    "time_horizon": 1.0,      # 1 year
    "num_time_steps": 252,    # Daily steps for 1 year
    "num_paths": 1000
}

# Example plot_options to enable only inflation rate paths plot
plot_options = {
    "inflation_rate_paths": {"enabled": True, "output_filename": "my_custom_inflation_paths.html"},
    "inflation_rate_distribution_at_maturity": {"enabled": False} # Disable distribution plot
}

simulation_result = inflation_model.simulate(scenario_definition, plot_options=plot_options)
```

If `plot_options` is not provided, default plots (inflation rate paths and distribution) will be generated. You can enable or disable specific plots and customize their output filenames. The method returns an `InflationSimulationResult` object for immediate in-memory use, and the primary output (`simulated_inflation_rates.csv`) along with the specified plots are saved to the output directory (`RiskModels/data/outputs/inflation_model/`).

#### **B. In-Memory Output (Internal `_simulate_logic()` method)**

For direct programmatic control without file I/O, you can call the internal `_simulate_logic` method. This method requires an `InflationInputData` object and `correlated_shocks` (which must be provided, not generated internally).

```python
from models.Inflation_Risk.mean_reverting_model.model import MeanRevertingInflationModel
from models.Inflation_Risk.mean_reverting_model.data_structures import InflationInputData

inflation_model = MeanRevertingInflationModel()

input_data = InflationInputData(
    initial_inflation_rate=0.02,
    long_term_mean_inflation_rate=0.03,
    mean_reversion_speed=0.5,
    volatility=0.01,
    time_horizon=1.0,
    num_time_steps=252,
    num_paths=1000
)

# Example of generating correlated shocks
num_timesteps = input_data.num_time_steps
num_paths = input_data.num_paths
correlated_shocks_array = np.random.standard_normal(size=(num_timesteps, num_paths))

simulation_result = inflation_model._simulate_logic(input_data, correlated_shocks_array)
```

This method returns an `InflationSimulationResult` object directly, without saving any files.

#### **Output of Simulation**

Both methods return an `InflationSimulationResult` object. This object contains:

*   `paths`: A large table (NumPy array) of the simulated inflation rate paths.
*   `time_grid`: A list of the time points corresponding to the rows in the `paths` table.

You can now use this `paths` table for further analysis, pricing, and other calculations.

---

### **4. Using the API Endpoint (Recommended for Most Users)**

With the new RiskModels API, you can run the Mean-Reverting Inflation model securely and easily from your browser or any tool that can make web requests. This is the recommended way for most users, especially non-programmers.

#### **A. How to Use the API**

1. **Log in to the API** using your username and password to get your access token.
2. **Go to the API documentation page:**
   - Open your browser and visit: `http://127.0.0.1:8000/docs`
   - This page lets you try out the inflation model interactively.
3. **Find the `/api/run/mean_reverting_inflation_model` endpoint.**
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
You can now run the Mean-Reverting Inflation model from your browser, securely and easily, without writing any code. For advanced use, you can still use the Python interfaces described above.
