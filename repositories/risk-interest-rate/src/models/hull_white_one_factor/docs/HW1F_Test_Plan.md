# Test Plan
### Model Plugin: Hull-White One-Factor (HW1F)
**Version:** 1.1
**Date:** 28 June 2025

## 1. Introduction

#### 1.1 Purpose
This document describes the testing strategy for the **Hull-White One-Factor (HW1F) Model Plugin**. Its purpose is to verify that the plugin is implemented correctly according to its Software Requirements Specification (SRS) and Software Design Document (SDD), and that it functions as a reliable component of the larger ESG platform.

#### 1.2 Scope
This plan covers unit, integration, validation, and performance testing of the HW1F plugin. It does not cover testing of the Core Engine or other platform components, which will have their own test plans.

## 2. Testing Strategy & Environment

*   **Framework:** All tests will be written using the **`pytest`** framework.
*   **Fixtures:** `pytest` fixtures (e.g., `tmp_path`) will be used extensively to create isolated, temporary environments for tests that require file I/O.
*   **Automation:** Tests will be structured to run automatically as part of the platform's CI/CD pipeline.

## 3. Test Cases

### 3.1. Unit Tests

*   **Target:** `formulas.py`
    *   **TC-U-01:** Test the `B(t, T, a)` function with known parameters `(t, T, a)` and assert that the output matches a pre-calculated value.
    *   **TC-U-02:** Test the `B(t, T, a)` function with an edge case where `t = T`. The expected output is `0`.

*   **Target:** `pricing.py`
    *   **TC-U-03:** Test the `price_zcb` function. This will require a mock `CalibratedHW1FModel` object with known parameters. The test will assert that the output price matches a pre-calculated value.

*   **Target:** `model.py`
    *   **TC-U-04:** Test the `get_name()` method. Assert that it returns the correct string `"hull_white_one_factor"`.
    *   **TC-U-05:** Test the `get_required_risk_factors()` method. Assert that it returns the correct list of strings.
    *   **TC-U-06:** Test the `train()` method. Assert that calling this method raises a `NotImplementedError`.
    *   **TC-U-07:** Test the `predict()` method. Assert that calling this method raises a `NotImplementedError`.

### 3.2. Integration Tests (File I/O)

*   **Target:** `model.py` (`calibrate` method)
    *   **TC-I-01: Test Calibration with File Input**
        *   **Description:** Verify that the `calibrate` method can successfully read input files and run without errors.
        *   **Setup:** Use the `pytest` `tmp_path` fixture to create temporary input and output directories.
        *   **Steps:**
            1.  Create dummy `initial_zcb_curve.csv` and `swaption_volatilities.csv` files in the temporary input directory.
            2.  Instantiate the `HullWhiteOneFactor` model, pointing it to the temporary directories.
            3.  Use `pytest-mock` to mock the `scipy.optimize.minimize` call to return a successful result immediately.
            4.  Call the `calibrate()` method.
            5.  Assert that the method returns a `CalibratedHW1FModel` object and does not raise an exception.

*   **Target:** `model.py` (`simulate` method)
    *   **TC-I-02: Test Simulation with File Output**
        *   **Description:** Verify that the `simulate` method correctly writes its output to a CSV file.
        *   **Setup:** Use the `pytest` `tmp_path` fixture. Create a mock `CalibratedHW1FModel` object.
        *   **Steps:**
            1.  Instantiate the `HullWhiteOneFactor` model, pointing it to the temporary directories.
            2.  Define a `scenario_definition` dictionary.
            3.  Call the `simulate()` method with the mock calibrated model and scenario definition.
            4.  Assert that the `simulated_yield_curves.csv` file is created in the temporary output directory.
            5.  Assert that the returned `HW1FSimulationResult` object contains a NumPy array of the correct dimensions.

### 3.3. Validation Tests (Financial Correctness)

*   **TC-V-01: Yield Curve Fit Verification**
    *   **Description:** After a successful calibration, the model must perfectly reproduce the initial yield curve it was calibrated to.
    *   **Setup:** Create a known yield curve in a temporary `initial_zcb_curve.csv` file.
    *   **Steps:**
        1.  Run the `calibrate` method.
        2.  Using the resulting `CalibratedHW1FModel` object, call the `price_zcb` function for each tenor on the original yield curve.
        3.  Assert that the model-generated ZCB prices are equal to the market ZCB prices to within a small tolerance (e.g., `1e-9`).

*   **TC-V-02: Short Rate Distribution Test**
    *   **Description:** The simulated short rate `r(T)` at a future time `T` should be normally distributed with a known analytical mean and variance.
    *   **Steps:**
        1.  Run the `simulate` method for a large number of paths (e.g., 50,000).
        2.  Extract the simulated rates `r(T)` at a specific future time step `T`.
        3.  Calculate the analytical mean and variance of `r(T)`.
        4.  Assert that the sample mean and variance of the simulated rates are close to the analytical values.

*   **TC-V-03: Martingale Test for ZCB**
    *   **Description:** The discounted price of a ZCB must be a martingale under the risk-neutral measure.
    *   **Steps:**
        1.  Price a ZCB at time 0, `P(0,T)`.
        2.  Run a simulation to get paths of the short rate `r(t)`.
        3.  For each path, calculate the discounted ZCB price at a future time `t_i < T`.
        4.  Calculate the average of these discounted prices across all simulation paths.
        5.  Assert that this average is close to the initial price `P(0,T)`.

### 3.4. Performance Tests

*   **TC-P-01: Calibration Performance**
    *   **Description:** Verify that the calibration process meets the performance requirement.
    *   **Steps:**
        1.  Create a test case with a realistic set of 20 swaption instruments in a temporary CSV file.
        2.  Use `pytest-benchmark` to measure the execution time of the `calibrate` method.
        3.  Assert that the mean execution time is less than 30 seconds.

*   **TC-P-02: Simulation Performance**
    *   **Description:** Verify that the simulation process meets the performance requirement.
    *   **Steps:**
        1.  Create a test case to simulate 10,000 paths over a 50-year horizon with monthly steps.
        2.  Use `pytest-benchmark` to measure the execution time of the `simulate` method.
        3.  Assert that the mean execution time is less than 60 seconds.
