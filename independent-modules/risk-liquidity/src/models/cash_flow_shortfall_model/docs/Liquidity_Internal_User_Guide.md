### **Internal User Guide (Draft): Cash Flow Shortfall Model**

**Version:** 1.0
**Date:** 28 June 2025
**Purpose:** This document describes how to use the `CashFlowShortfallModel` plugin, focusing on its dual interface for both file-based and in-memory data operations.

---

### **1. Overview**

The Cash Flow Shortfall Model is a tool for assessing liquidity risk by projecting cash inflows and outflows over a specified period. It identifies potential shortfalls where cumulative outflows exceed cumulative inflows, indicating a need for additional liquidity.

Using the model primarily involves:
1.  **Prepare Input Data:** Provide historical or projected cash flow data, either through a CSV file or directly in memory.
2.  **Run Calculation:** Calculate net cash flows, cumulative cash flows, and identify shortfalls.

---

### **2. Data Input and Output**

The model offers two primary ways to interact with data:

**A. File-Based I/O (Convenience for Standalone Use)**
For ease of use and to avoid hardcoding, the model can read its inputs from and write its outputs to a standardized directory structure.

*   **Input Directory:** `RiskModels/data/inputs/liquidity_model/`
*   **Output Directory:** `RiskModels/data/outputs/liquidity_model/`

#### **Input File Formats**

The model expects the following CSV file in the input directory:

**a) `cash_flows.csv`**
*   **Purpose:** Defines the cash inflows and outflows over time.
*   **Format:** A CSV file with the following columns:
    *   `Date`: The date or period identifier (e.g., YYYY-MM-DD).
    *   `Inflows`: Cash received during the period.
    *   `Outflows`: Cash paid out during the period.

    ```csv
    Date,Inflows,Outflows
    2025-01-31,1000,800
    2025-02-28,1200,1500
    2025-03-31,900,700
    ```

#### **Output File Format**

The model saves its primary calculation results and generated plots to the output directory.

**a) `cash_flow_results.csv`**
*   **Purpose:** Stores the calculated net cash flow, cumulative cash flow, and identified shortfalls.
*   **Format:** A CSV file with the original input columns plus:
    *   `Net_Cash_Flow`: `Inflows - Outflows`.
    *   `Cumulative_Cash_Flow`: Running total of `Net_Cash_Flow`.
    *   `Shortfall`: Boolean (True if `Cumulative_Cash_Flow` is negative, False otherwise).

    ```csv
    Date,Inflows,Outflows,Net_Cash_Flow,Cumulative_Cash_Flow,Shortfall
    2025-01-31,1000,800,200,200,False
    2025-02-28,1200,1500,-300,-100,True
    2025-03-31,900,700,200,100,False
    ```

**b) `net_cash_flow_plot.html`**
*   **Purpose:** An interactive HTML plot visualizing the net cash flow for each period.
*   **Format:** An HTML file that can be opened directly in a web browser.

**c) `cumulative_cash_flow_plot.html`**
*   **Purpose:** An interactive HTML plot visualizing the cumulative cash flow over time, highlighting periods of shortfall.
*   **Format:** An HTML file that can be opened directly in a web browser.

**B. In-Memory Data (For Core Engine Integration)**
For direct integration with the Core Engine or other Python modules, the model also exposes internal logic methods that operate directly on in-memory data structures. This avoids file I/O overhead for real-time or programmatic use.

---

### **3. Step 1: Calculating Cash Flow Shortfall**

**Goal:** To calculate and identify potential liquidity shortfalls.

#### **A. Using File-Based Input (Public `calculate()` method)**

This is done by calling the public `calculate` method. It can take an optional `scenario_definition` dictionary (for future use, e.g., filtering data) and `plot_options`.

```python
from models.Liquidity_Risk.cash_flow_shortfall_model.model import CashFlowShortfallModel

liquidity_model = CashFlowShortfallModel()

# Example plot_options to enable only cumulative cash flow plot
plot_options = {
    "net_cash_flow_plot": {"enabled": False},
    "cumulative_cash_flow_plot": {"enabled": True, "output_filename": "my_custom_cumulative_cf.html"}
}

results = liquidity_model.calculate(plot_options=plot_options)
```

If `plot_options` is not provided, default plots (net cash flow and cumulative cash flow) will be generated. You can enable or disable specific plots and customize their output filenames. The method returns a `CashFlowResults` object for immediate in-memory use, and the primary output (`cash_flow_results.csv`) along with the specified plots are saved to the output directory (`RiskModels/data/outputs/liquidity_model/`).

#### **B. In-Memory Output (Internal `_calculate_logic()` method)**

For direct programmatic control without file I/O, you can call the internal `_calculate_logic` method. This method requires a `CashFlowInputData` object.

```python
from models.Liquidity_Risk.cash_flow_shortfall_model.model import CashFlowShortfallModel
from models.Liquidity_Risk.cash_flow_shortfall_model.data_structures import CashFlowInputData
import pandas as pd

liquidity_model = CashFlowShortfallModel()

# Example of in-memory input data
input_df = pd.DataFrame({
    'Date': pd.to_datetime(['2025-01-31', '2025-02-28', '2025-03-31']),
    'Inflows': [1000, 1200, 900],
    'Outflows': [800, 1500, 700]
})
input_data = CashFlowInputData(cash_flows_df=input_df)

results = liquidity_model._calculate_logic(input_data)

print(results.results_df)
```

This method returns a `CashFlowResults` object directly, without saving any files.

#### **Output of Calculation**

Both methods return a `CashFlowResults` object. This object contains:

*   `results_df`: A Pandas DataFrame with the original input data plus calculated `Net_Cash_Flow`, `Cumulative_Cash_Flow`, and `Shortfall` columns.

You can now use this DataFrame for further analysis and reporting.

---

### **4. Using the API Endpoint (Recommended for Most Users)**

With the new RiskModels API, you can run the Cash Flow Shortfall model securely and easily from your browser or any tool that can make web requests. This is the recommended way for most users, especially non-programmers.

#### **A. How to Use the API**

1. **Log in to the API** using your username and password to get your access token.
2. **Go to the API documentation page:**
   - Open your browser and visit: `http://127.0.0.1:8000/docs`
   - This page lets you try out the Cash Flow Shortfall model interactively.
3. **Find the `/api/run/cash_flow_shortfall_model` endpoint.**
4. **(Optional) Fill in any scenario parameters** (future versions may support more options).
5. **Authorize with your token** (click "Authorize" in the docs UI and paste your token).
6. **Click "Execute"** to run the calculation.
7. **View or download the results** (returned as JSON for easy use in Excel, Python, R, etc.).

#### **B. Where to Find More Help**
- See the [API Quick Start Guide](../../../../docs/guides/quickstart_api.md) for a plain-English walkthrough and more details.
- The API is secure: only authenticated users can run models.

#### **C. Why Use the API?**
- No coding required—just fill in a form and get results.
- Works for both technical and non-technical users.
- Results are returned instantly and can be used in any analysis tool.

**In summary:**
You can now run the Cash Flow Shortfall model from your browser, securely and easily, without writing any code. For advanced use, you can still use the Python interfaces described above.
