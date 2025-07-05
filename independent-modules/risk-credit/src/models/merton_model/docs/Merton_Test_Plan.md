# Test Plan
### Model Plugin: Merton Model for Credit Risk
**Version:** 1.0
**Date:** 28 June 2025

## 1. Introduction

This document outlines the test plan for the **Merton Model Plugin**. It details the testing strategy, test cases, and expected outcomes to ensure the model's accuracy, reliability, and adherence to the specified requirements.

## 2. Testing Strategy

Testing will follow a multi-layered approach:

*   **Unit Testing:** Focus on individual functions and methods (e.g., `d1`, `d2`, `black_scholes_call`, `calculate_default_probability`, `calculate_credit_spread`) to ensure their correctness in isolation.
*   **Integration Testing:** Verify the interaction between different modules (e.g., `model.py` interacting with `formulas.py` and `calculations.py`, and file I/O).
*   **Validation Testing:** Compare the model's outputs against known analytical solutions, benchmark data, or established industry practices.
*   **Performance Testing:** Assess the model's computational efficiency for calibration and simulation.

## 3. Test Environment

*   **Operating System:** Cross-platform (Windows, Linux, macOS).
*   **Python Version:** Consistent with project standards.
*   **Dependencies:** All required Python libraries (NumPy, SciPy, Pandas) installed.

## 4. Test Cases

### 4.1. Unit Tests

#### **Target: `formulas.py`**

*   **TC-U-01: `d1` and `d2` Calculation:**
    *   **Description:** Verify `d1` and `d2` functions with various valid inputs (positive, zero, negative values for parameters).
    *   **Input:** Specific values for S, K, T, r, sigma.
    *   **Expected Output:** Calculated `d1` and `d2` values match analytical or pre-calculated results.
*   **TC-U-02: `black_scholes_call` Calculation:**
    *   **Description:** Verify `black_scholes_call` function with various valid inputs.
    *   **Input:** Specific values for S, K, T, r, sigma.
    *   **Expected Output:** Calculated call option price matches analytical or pre-calculated results.

#### **Target: `calculations.py`**

*   **TC-U-03: `calculate_default_probability`:**
    *   **Description:** Verify default probability calculation for various scenarios (e.g., deep in/out of the money, short/long time to maturity).
    *   **Input:** Calibrated asset value, asset volatility, face value of debt, time to maturity, risk-free rate.
    *   **Expected Output:** Calculated PD matches analytical or pre-calculated results.
*   **TC-U-04: `calculate_credit_spread`:**
    *   **Description:** Verify credit spread calculation.
    *   **Input:** Calibrated asset value, asset volatility, face value of debt, time to maturity, risk-free rate (and assumed recovery rate if applicable).
    *   **Expected Output:** Calculated credit spread matches analytical or pre-calculated results.

#### **Target: `model.py` (Basic Methods)**

*   **TC-U-05: `get_name()`:**
    *   **Description:** Verify the model returns its correct name.
    *   **Expected Output:** "merton_model".
*   **TC-U-06: `get_required_risk_factors()`:**
    *   **Description:** Verify the model returns the correct list of required risk factors.
    *   **Expected Output:** `["equity_value", "equity_volatility", "face_value_debt", "time_to_maturity", "risk_free_rate"]`.
*   **TC-U-07: `train()` and `predict()` raise `NotImplementedError`:**
    *   **Description:** Confirm that `train` and `predict` methods raise `NotImplementedError` as they are not applicable to this model.

### 4.2. Integration Tests

*   **TC-I-01: `calibrate()` Public Method (File-Based I/O):**
    *   **Description:** Test the public `calibrate()` method, ensuring it correctly loads data from `firm_data.csv` and calls the internal calibration logic.
    *   **Setup:** Create a dummy `firm_data.csv` in a temporary input directory.
    *   **Expected Output:** A `CalibratedMertonModel` object is returned, and the internal `_calibrate_logic` is invoked with correct data.
*   **TC-I-02: `_load_and_prepare_data()`:**
    *   **Description:** Verify the internal data loading and preparation function.
    *   **Setup:** Create a dummy `firm_data.csv`.
    *   **Expected Output:** Returns a `MertonInputData` object with correct values.
*   **TC-I-03: `_calibrate_logic()`:**
    *   **Description:** Test the core calibration logic with in-memory data.
    *   **Input:** `MertonInputData` object.
    *   **Expected Output:** Returns a `CalibratedMertonModel` object with implied asset value and volatility that satisfy the Merton model equations.
*   **TC-I-04: `_calculate_results_logic()`:**
    *   **Description:** Test the calculation of PD and Credit Spread with in-memory data.
    *   **Input:** `CalibratedMertonModel` and `MertonInputData` objects.
    *   **Expected Output:** Returns a `MertonOutputResults` object with correct PD and Credit Spread values.
*   **TC-I-05: End-to-End Calculation (File-to-File):**
    *   **Description:** Test the full workflow from loading data from file, calibrating, calculating results, and saving to an output file.
    *   **Setup:** Dummy `firm_data.csv`.
    *   **Expected Output:** `merton_results.csv` is created with expected output values.
*   **TC-I-06: `_simulate_logic()`:**
    *   **Description:** Test the core simulation logic with in-memory data.
    *   **Input:** `CalibratedMertonModel` object, `scenario_definition` (time horizon, number of time steps, number of paths), and optional `correlated_shocks`.
    *   **Expected Output:** Returns a `MertonSimulationResult` object with correct dimensions for paths and time grid, and appropriate default events.
*   **TC-I-07: `simulate()` Public Method (File-Based I/O and Plotting):**
    *   **Description:** Test the public `simulate()` method, ensuring it correctly performs simulation, saves results to CSV, and generates plots based on `plot_options`.
    *   **Setup:** Create a mock `CalibratedMertonModel` object.
    *   **Input:** `scenario_definition` and various `plot_options` configurations.
    *   **Expected Output:** `simulated_asset_paths.csv` is created, and specified HTML plot files are generated.

### 4.3. Validation Tests

*   **TC-V-01: Known Analytical Solution Verification (Calibration & Calculation):**
    *   **Description:** Compare the model's calibrated asset value, asset volatility, PD, and credit spread against known analytical solutions for specific input parameters.
    *   **Input:** Carefully chosen input parameters for which analytical solutions exist.
    *   **Expected Output:** Model outputs match analytical solutions within a defined tolerance.
*   **TC-V-02: Sensitivity Analysis (Calibration & Calculation):**
    *   **Description:** Test the sensitivity of PD and credit spread to changes in input parameters (e.g., increase equity volatility, decrease time to maturity).
    *   **Expected Output:** Outputs change in the expected direction and magnitude.
*   **TC-V-03: Simulated Asset Path Properties:**
    *   **Description:** Verify that the simulated asset paths exhibit properties consistent with Geometric Brownian Motion (e.g., log-normality of asset values at maturity).
    *   **Input:** Large number of simulation paths.
    *   **Expected Output:** Statistical properties of simulated paths (mean, variance of log-returns) are close to theoretical values.
*   **TC-V-04: Default Event Consistency:**
    *   **Description:** Verify that default events are correctly identified based on the simulated asset paths crossing the debt threshold.
    *   **Input:** Simulated asset paths and debt value.
    *   **Expected Output:** Number of defaults and timing of defaults are consistent with expectations.

### 4.4. Performance Tests

*   **TC-P-01: Calibration Performance:**
    *   **Description:** Measure the time taken for the `calibrate()` method to execute for a typical input size.
    *   **Expected Outcome:** Calibration time is within acceptable limits (e.g., < 1 second).
*   **TC-P-02: Calculation Performance:**
    *   **Description:** Measure the time taken for `_calculate_results_logic()` to execute.
    *   **Expected Outcome:** Calculation time is negligible.
*   **TC-P-03: Simulation Performance:**
    *   **Description:** Measure the time taken for the `simulate()` method to execute for a typical input size (large number of paths and time steps).
    *   **Expected Outcome:** Simulation time is within acceptable limits.

## 5. Test Reporting

Test results will be reported using `pytest`'s standard output. For performance tests, `pytest-benchmark` will be used to generate detailed reports.

### 4.2. Integration Tests

*   **TC-I-01: `calibrate()` Public Method (File-Based I/O):**
    *   **Description:** Test the public `calibrate()` method, ensuring it correctly loads data from `firm_data.csv` and calls the internal calibration logic.
    *   **Setup:** Create a dummy `firm_data.csv` in a temporary input directory.
    *   **Expected Output:** A `CalibratedMertonModel` object is returned, and the internal `_calibrate_logic` is invoked with correct data.
*   **TC-I-02: `_load_and_prepare_data()`:**
    *   **Description:** Verify the internal data loading and preparation function.
    *   **Setup:** Create a dummy `firm_data.csv`.
    *   **Expected Output:** Returns a `MertonInputData` object with correct values.
*   **TC-I-03: `_calibrate_logic()`:**
    *   **Description:** Test the core calibration logic with in-memory data.
    *   **Input:** `MertonInputData` object.
    *   **Expected Output:** Returns a `CalibratedMertonModel` object with implied asset value and volatility that satisfy the Merton model equations.
*   **TC-I-04: `_calculate_results_logic()`:**
    *   **Description:** Test the calculation of PD and Credit Spread with in-memory data.
    *   **Input:** `CalibratedMertonModel` and `MertonInputData` objects.
    *   **Expected Output:** Returns a `MertonOutputResults` object with correct PD and Credit Spread values.
*   **TC-I-05: End-to-End Calculation (File-to-File):**
    *   **Description:** Test the full workflow from loading data from file, calibrating, calculating results, and saving to an output file.
    *   **Setup:** Dummy `firm_data.csv`.
    *   **Expected Output:** `merton_results.csv` is created with expected output values.

### 4.3. Validation Tests

*   **TC-V-01: Known Analytical Solution Verification:**
    *   **Description:** Compare the model's calibrated asset value, asset volatility, PD, and credit spread against known analytical solutions for specific input parameters.
    *   **Input:** Carefully chosen input parameters for which analytical solutions exist.
    *   **Expected Output:** Model outputs match analytical solutions within a defined tolerance.
*   **TC-V-02: Sensitivity Analysis:**
    *   **Description:** Test the sensitivity of PD and credit spread to changes in input parameters (e.g., increase equity volatility, decrease time to maturity).
    *   **Expected Output:** Outputs change in the expected direction and magnitude.

### 4.4. Performance Tests

*   **TC-P-01: Calibration Performance:**
    *   **Description:** Measure the time taken for the `calibrate()` method to execute for a typical input size.
    *   **Expected Outcome:** Calibration time is within acceptable limits (e.g., < 1 second).
*   **TC-P-02: Calculation Performance:**
    *   **Description:** Measure the time taken for `_calculate_results_logic()` to execute.
    *   **Expected Outcome:** Calculation time is negligible.

## 5. Test Reporting

Test results will be reported using `pytest`'s standard output. For performance tests, `pytest-benchmark` will be used to generate detailed reports.
