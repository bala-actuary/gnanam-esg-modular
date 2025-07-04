### **Internal User Guide (Draft): Basic Exposure Model**

**Version:** 1.0
**Date:** 28 June 2025
**Purpose:** This document describes how to use the `BasicExposureModel` plugin, focusing on its dual interface for both file-based and in-memory data operations.

---

### **1. Overview**

The Basic Exposure Model is a tool for calculating the current exposure to individual counterparties based on a portfolio of trades. It aggregates market values of trades to determine total, positive, and negative exposures.

Using the model primarily involves:
1.  **Prepare Input Data:** Provide a portfolio of trades with market values, either through a CSV file or directly in memory.
2.  **Run Calculation:** Calculate the exposures for each counterparty.

---

### **2. Data Input and Output**

The model offers two primary ways to interact with data:

**A. File-Based I/O (Convenience for Standalone Use)**
For ease of use and to avoid hardcoding, the model can read its inputs from and write its outputs to a standardized directory structure.

*   **Input Directory:** `RiskModels/data/inputs/counterparty_risk/`
*   **Output Directory:** `RiskModels/data/outputs/counterparty_risk/`

#### **Input File Formats**

The model expects the following CSV file in the input directory:

**a) `trades_portfolio.csv`**
*   **Purpose:** Defines the portfolio of trades.
*   **Format:** A CSV file with the following columns:
    *   `Counterparty_ID`: Unique identifier for the counterparty.
    *   `Trade_ID`: Unique identifier for the trade.
    *   `Market_Value`: Current market value of the trade (positive for assets, negative for liabilities).

    ```csv
    Counterparty_ID,Trade_ID,Market_Value
    CP001,TRD001,1000
    CP001,TRD002,-500
    CP002,TRD003,2000
    ```

#### **Output File Format**

The model saves its primary calculation results and generated plots to the output directory.

**a) `exposure_results.csv`**
*   **Purpose:** Stores the calculated total, positive, and negative exposures per counterparty.
*   **Format:** A CSV file with the following columns:
    *   `Counterparty_ID`
    *   `Total_Exposure`: Sum of all market values for the counterparty.
    *   `Positive_Exposure`: Sum of positive market values for the counterparty.
    *   `Negative_Exposure`: Sum of negative market values for the counterparty.

    ```csv
    Counterparty_ID,Total_Exposure,Positive_Exposure,Negative_Exposure
    CP001,500,1000,-500
    CP002,2000,2000,0
    ```

**b) `exposure_plot.html`**
*   **Purpose:** An interactive HTML plot visualizing exposures per counterparty (e.g., a stacked bar chart).
*   **Format:** An HTML file that can be opened directly in a web browser.

**B. In-Memory Data (For Core Engine Integration)**
For direct integration with the Core Engine or other Python modules, the model also exposes internal logic methods that operate directly on in-memory data structures. This avoids file I/O overhead for real-time or programmatic use.

---

### **3. Step 1: Calculating Counterparty Exposure**

**Goal:** To calculate and identify exposures to individual counterparties.

#### **A. Using File-Based Input (Public `calculate()` method)**

This is done by calling the public `calculate` method. It can take an optional `scenario_definition` dictionary (for future use, e.g., filtering data) and `plot_options`.

```python
from models.Counterparty_Risk.basic_exposure_model.model import BasicExposureModel

exposure_model = BasicExposureModel()

# Example plot_options to enable the exposure plot
plot_options = {
    "exposure_plot": {"enabled": True, "output_filename": "my_custom_exposure_plot.html"}
}

results = exposure_model.calculate(plot_options=plot_options)
```

If `plot_options` is not provided, a default exposure plot will be generated. You can enable or disable specific plots and customize their output filenames. The method returns an `ExposureResults` object for immediate in-memory use, and the primary output (`exposure_results.csv`) along with the specified plots are saved to the output directory (`RiskModels/data/outputs/counterparty_risk/`).

#### **B. In-Memory Output (Internal `_calculate_logic()` method)**

For direct programmatic control without file I/O, you can call the internal `_calculate_logic` method. This method requires a `TradePortfolioInputData` object.

```python
from models.Counterparty_Risk.basic_exposure_model.model import BasicExposureModel
from models.Counterparty_Risk.basic_exposure_model.data_structures import TradePortfolioInputData
import pandas as pd

exposure_model = BasicExposureModel()

# Example of in-memory input data
input_df = pd.DataFrame({
    'Counterparty_ID': ['CP001', 'CP001', 'CP002'],
    'Trade_ID': ['TRD001', 'TRD002', 'TRD003'],
    'Market_Value': [1000, -500, 2000]
})
input_data = TradePortfolioInputData(portfolio_df=input_df)

results = exposure_model._calculate_logic(input_data)

print(results.results_df)
```

This method returns an `ExposureResults` object directly, without saving any files.

#### **Output of Calculation**

Both methods return an `ExposureResults` object. This object contains:

*   `results_df`: A Pandas DataFrame with the calculated `Total_Exposure`, `Positive_Exposure`, and `Negative_Exposure` for each `Counterparty_ID`.

You can now use this DataFrame for further analysis and reporting.

---

### **4. Using the API Endpoint (Recommended for Most Users)**

With the new RiskModels API, you can run the Basic Exposure model securely and easily from your browser or any tool that can make web requests. This is the recommended way for most users, especially non-programmers.

#### **A. How to Use the API**

1. **Log in to the API** using your username and password to get your access token.
2. **Go to the API documentation page:**
   - Open your browser and visit: `http://127.0.0.1:8000/docs`
   - This page lets you try out the Basic Exposure model interactively.
3. **Find the `/api/run/basic_exposure_model` endpoint.**
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
You can now run the Basic Exposure model from your browser, securely and easily, without writing any code. For advanced use, you can still use the Python interfaces described above.
