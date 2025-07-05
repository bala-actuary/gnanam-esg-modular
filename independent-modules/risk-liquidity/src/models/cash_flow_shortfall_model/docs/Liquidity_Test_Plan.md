# Test Plan
### Model Plugin: Cash Flow Shortfall Model for Liquidity Risk
**Version:** 1.0
**Date:** 28 June 2025

## 1. Introduction

This document outlines the test plan for the **Cash Flow Shortfall Model Plugin**. It details the testing strategy, test cases, and expected outcomes to ensure the model's accuracy, reliability, and adherence to the specified requirements.

## 2. Testing Strategy

Testing will follow a multi-layered approach:

*   **Unit Testing:** Focus on individual functions and methods (e.g., `calculate_net_cash_flow`, `calculate_cumulative_cash_flow`, `identify_shortfalls`) to ensure their correctness in isolation.
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

*   **TC-U-01: `calculate_net_cash_flow`:**
    *   **Description:** Verify net cash flow calculation for various inflow and outflow scenarios.
    *   **Input:** `pd.Series` of inflows and outflows.
    *   **Expected Output:** `pd.Series` of net cash flows matching expected values.
*   **TC-U-02: `calculate_cumulative_cash_flow`:**
    *   **Description:** Verify cumulative cash flow calculation.
    *   **Input:** `pd.Series` of net cash flows.
    *   **Expected Output:** `pd.Series` of cumulative cash flows matching expected values.
*   **TC-U-03: `identify_shortfalls`:**
    *   **Description:** Verify shortfall identification for various cumulative cash flow scenarios.
    *   **Input:** `pd.Series` of cumulative cash flows.
    *   **Expected Output:** `pd.Series` of boolean values (True for shortfall, False otherwise) matching expected values.

#### **Target: `model.py` (Basic Methods)**

*   **TC-U-04: `get_name()`:**
    *   **Description:** Verify the model returns its correct name.
    *   **Expected Output:** "cash_flow_shortfall_model".
*   **TC-U-05: `get_required_risk_factors()`:**
    *   **Description:** Verify the model returns the correct list of required risk factors.
    *   **Expected Output:** `["cash_inflows", "cash_outflows", "time_horizon", "frequency"]`.
*   **TC-U-06: `calibrate()`, `simulate()`, `train()`, `predict()` raise `NotImplementedError`:**
    *   **Description:** Confirm that these methods raise `NotImplementedError` as they are not applicable to this model.

### 4.2. Integration Tests

*   **TC-I-01: `_load_and_prepare_data()`:**
    *   **Description:** Verify the internal data loading and preparation function.
    *   **Setup:** Create a dummy `cash_flows.csv`.
    *   **Expected Output:** Returns a `CashFlowInputData` object with a DataFrame containing correct data and parsed dates.
*   **TC-I-02: `_calculate_logic()`:**
    *   **Description:** Test the core calculation logic with in-memory data.
    *   **Input:** `CashFlowInputData` object.
    *   **Expected Output:** Returns a `CashFlowResults` object with a DataFrame containing correct `Net_Cash_Flow`, `Cumulative_Cash_Flow`, and `Shortfall` columns.
*   **TC-I-03: `calculate()` Public Method (File-Based I/O and Plotting):**
    *   **Description:** Test the public `calculate()` method, ensuring it correctly loads data, performs calculations, saves results to CSV, and generates plots based on `plot_options`.
    *   **Setup:** Create a dummy `cash_flows.csv` in a temporary input directory.
    *   **Input:** `scenario_definition` (optional) and various `plot_options` configurations.
    *   **Expected Output:** `cash_flow_results.csv` is created, and specified HTML plot files are generated.

### 4.3. Validation Tests

*   **TC-V-01: Manual Calculation Verification:**
    *   **Description:** Compare the model's calculated net cash flow, cumulative cash flow, and shortfalls against a small, manually calculated example.
    *   **Input:** Simple `cash_flows.csv` with clear inflows and outflows.
    *   **Expected Output:** All calculated columns match manual results precisely.

### 4.4. Performance Tests

*   **TC-P-01: Calculation Performance:**
    *   **Description:** Measure the time taken for the `calculate()` method to execute for a typical input size (large number of cash flow periods).
    *   **Expected Outcome:** Calculation time is within acceptable limits.

## 5. Test Reporting

Test results will be reported using `pytest`'s standard output. For performance tests, `pytest-benchmark` will be used to generate detailed reports.
