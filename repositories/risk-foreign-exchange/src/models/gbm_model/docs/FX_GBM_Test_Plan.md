# Test Plan
### Model Plugin: Geometric Brownian Motion (GBM) Model for Foreign Exchange Risk
**Version:** 1.0
**Date:** 28 June 2025

## 1. Introduction

This document outlines the test plan for the **Geometric Brownian Motion (GBM) Model Plugin for Foreign Exchange Risk**. It details the testing strategy, test cases, and expected outcomes to ensure the model's accuracy, reliability, and adherence to the specified requirements.

## 2. Testing Strategy

Testing will follow a multi-layered approach:

*   **Unit Testing:** Focus on individual functions and methods (e.g., `fx_gbm_step`) to ensure their correctness in isolation.
*   **Integration Testing:** Verify the interaction between different modules (e.g., `model.py` interacting with `formulas.py`, and file I/O).
*   **Validation Testing:** Compare the model's outputs against known analytical properties of GBM (e.g., expected mean and variance of log-exchange rates).
*   **Performance Testing:** Assess the model's computational efficiency for simulation.

## 3. Test Environment

*   **Operating System:** Cross-platform (Windows, Linux, macOS).
*   **Python Version:** Consistent with project standards.
*   **Dependencies:** All required Python libraries (NumPy, Pandas, Plotly) installed.

## 4. Test Cases

### 4.1. Unit Tests

#### **Target: `formulas.py`**

*   **TC-U-01: `fx_gbm_step` Calculation:**
    *   **Description:** Verify `fx_gbm_step` function with various valid inputs.
    *   **Input:** Specific values for `S_t`, `r_d`, `r_f`, `sigma`, `dt`, `dW`.
    *   **Expected Output:** Calculated `S_t+dt` matches analytical or pre-calculated results.

#### **Target: `model.py` (Basic Methods)**

*   **TC-U-02: `get_name()`:**
    *   **Description:** Verify the model returns its correct name.
    *   **Expected Output:** "fx_gbm_model".
*   **TC-U-03: `get_required_risk_factors()`:**
    *   **Description:** Verify the model returns the correct list of required risk factors.
    *   **Expected Output:** `["initial_exchange_rate", "domestic_risk_free_rate", "foreign_risk_free_rate", "volatility", "time_horizon", "num_time_steps", "num_paths"]`.
*   **TC-U-04: `calibrate()` raises `NotImplementedError`:**
    *   **Description:** Confirm that `calibrate` method raises `NotImplementedError` as it is not applicable to this model.
*   **TC-U-05: `train()` and `predict()` raise `NotImplementedError`:**
    *   **Description:** Confirm that `train` and `predict` methods raise `NotImplementedError` as they are not applicable to this model.

### 4.2. Integration Tests

*   **TC-I-01: `_load_and_prepare_data()`:**
    *   **Description:** Verify the internal data loading and preparation function, including overriding from `scenario_definition`.
    *   **Setup:** Create a dummy `fx_gbm_parameters.csv`.
    *   **Input:** `scenario_definition` with and without overriding parameters.
    *   **Expected Output:** Returns an `FXGBMInputData` object with correct values.
*   **TC-I-02: `_simulate_logic()`:**
    *   **Description:** Test the core simulation logic with in-memory data.
    *   **Input:** `FXGBMInputData` object and optional `correlated_shocks`.
    *   **Expected Output:** Returns an `FXGBMSimulationResult` object with correct dimensions and initial value.
*   **TC-I-03: `simulate()` Public Method (File-Based I/O and Plotting):**
    *   **Description:** Test the public `simulate()` method, ensuring it correctly loads data, performs simulation, saves results to CSV, and generates plots based on `plot_options`.
    *   **Setup:** Create a dummy `fx_gbm_parameters.csv` in a temporary input directory.
    *   **Input:** `scenario_definition` and various `plot_options` configurations.
    *   **Expected Output:** `simulated_exchange_rates.csv` is created, and specified HTML plot files are generated.

### 4.3. Validation Tests

*   **TC-V-01: Expected Mean of Log-Exchange Rates:**
    *   **Description:** Verify that the mean of the log-exchange rates at maturity across many paths is close to the analytically expected mean for FX GBM.
    *   **Input:** Large number of paths, specific FX GBM parameters.
    *   **Expected Output:** `mean(log(S_T))` is close to `log(S0) + (r_d - r_f - 0.5 * sigma^2) * T`.
*   **TC-V-02: Expected Variance of Log-Exchange Rates:**
    *   **Description:** Verify that the variance of the log-exchange rates at maturity across many paths is close to the analytically expected variance for FX GBM.
    *   **Input:** Large number of paths, specific FX GBM parameters.
    *   **Expected Output:** `var(log(S_T))` is close to `sigma^2 * T`.

### 4.4. Performance Tests

*   **TC-P-01: Simulation Performance:**
    *   **Description:** Measure the time taken for the `simulate()` method to execute for a typical input size (large number of paths and time steps).
    *   **Expected Outcome:** Simulation time is within acceptable limits.

## 5. Test Reporting

Test results will be reported using `pytest`'s standard output. For performance tests, `pytest-benchmark` will be used to generate detailed reports.
