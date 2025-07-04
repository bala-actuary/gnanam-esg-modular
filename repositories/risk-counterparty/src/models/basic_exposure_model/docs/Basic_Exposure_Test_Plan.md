# Test Plan
### Model Plugin: Basic Exposure Model for Counterparty Risk
**Version:** 1.0
**Date:** 28 June 2025

## 1. Introduction

This document outlines the test plan for the **Basic Exposure Model Plugin**. It details the testing strategy, test cases, and expected outcomes to ensure the model's accuracy, reliability, and adherence to the specified requirements.

## 2. Testing Strategy

Testing will follow a multi-layered approach:

*   **Unit Testing:** Focus on individual functions and methods (e.g., `calculate_counterparty_exposures`) to ensure their correctness in isolation.
*   **Integration Testing:** Verify the interaction between different modules (e.g., `model.py` interacting with `calculations.py`, and file I/O).
*   **Validation Testing:** Compare the model's outputs against manually calculated examples.
*   **Performance Testing:** Assess the model's computational efficiency for calculations.

## 3. Test Environment

*   **Operating System:** Cross-platform (Windows, Linux, macOS).
*   **Python Version:** Consistent with project standards.
*   **Dependencies:** All required Python libraries (NumPy, Pandas, Plotly) installed.

## 4. Test Cases

### 4.1. Unit Tests

#### **Target: `calculations.py`**

*   **TC-U-01: `calculate_counterparty_exposures`:**
    *   **Description:** Verify exposure calculations for various scenarios (positive, negative, mixed market values; single and multiple counterparties).
    *   **Input:** `pd.DataFrame` with `Counterparty_ID`, `Trade_ID`, `Market_Value`.
    *   **Expected Output:** `pd.DataFrame` with `Counterparty_ID`, `Total_Exposure`, `Positive_Exposure`, `Negative_Exposure` matching expected values.

#### **Target: `model.py` (Basic Methods)**

*   **TC-U-02: `get_name()`:**
    *   **Description:** Verify the model returns its correct name.
    *   **Expected Output:** "basic_exposure_model".
*   **TC-U-03: `get_required_risk_factors()`:**
    *   **Description:** Verify the model returns the correct list of required risk factors.
    *   **Expected Output:** `["trades_portfolio"]`.
*   **TC-U-04: `calibrate()`, `simulate()`, `train()`, `predict()` raise `NotImplementedError`:**
    *   **Description:** Confirm that these methods raise `NotImplementedError` as they are not applicable to this model.

### 4.2. Integration Tests

*   **TC-I-01: `_load_and_prepare_data()`:**
    *   **Description:** Verify the internal data loading and preparation function.
    *   **Setup:** Create a dummy `trades_portfolio.csv`.
    *   **Expected Output:** Returns a `TradePortfolioInputData` object with a DataFrame containing correct data.
*   **TC-I-02: `_calculate_logic()`:**
    *   **Description:** Test the core calculation logic with in-memory data.
    *   **Input:** `TradePortfolioInputData` object.
    *   **Expected Output:** Returns an `ExposureResults` object with a DataFrame containing correct exposure calculations.
*   **TC-I-03: `calculate()` Public Method (File-Based I/O and Plotting):**
    *   **Description:** Test the public `calculate()` method, ensuring it correctly loads data, performs calculations, saves results to CSV, and generates plots based on `plot_options`.
    *   **Setup:** Create a dummy `trades_portfolio.csv` in a temporary input directory.
    *   **Input:** `scenario_definition` (optional) and various `plot_options` configurations.
    *   **Expected Output:** `exposure_results.csv` is created, and specified HTML plot files are generated.

### 4.3. Validation Tests

*   **TC-V-01: Manual Calculation Verification:**
    *   **Description:** Compare the model's calculated exposures against a small, manually calculated example.
    *   **Input:** Simple `trades_portfolio.csv` with clear positive and negative market values.
    *   **Expected Output:** All calculated exposure columns match manual results precisely.

### 4.4. Performance Tests

*   **TC-P-01: Calculation Performance:**
    *   **Description:** Measure the time taken for the `calculate()` method to execute for a typical input size (large number of trades).
    *   **Expected Outcome:** Calculation time is within acceptable limits.

## 5. Test Reporting

Test results will be reported using `pytest`'s standard output. For performance tests, `pytest-benchmark` will be used to generate detailed reports.
