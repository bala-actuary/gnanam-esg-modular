# Software Requirements Specification (SRS)
### Model Plugin: Hull-White One-Factor (HW1F)
**Version:** 1.1
**Date:** 28 June 2025

## 1. Introduction

#### 1.1 Purpose
This document specifies the requirements for the **Hull-White One-Factor (HW1F) Model Plugin**. This plugin will be a self-contained component designed to integrate seamlessly with the "RiskModels" Integrated ESG Platform, as defined in the Platform Architecture Document (PAD).

#### 1.2 Scope
The scope of this plugin is limited to the implementation of the HW1F model itself. It will be responsible for calibration, pricing of specific derivatives, and simulation of the short-rate path, according to the `ModelInterface` contract.

*   **In Scope:**
    *   Implementing the HW1F mathematical formulas.
    *   Calibrating `a` and `σ` parameters from file-based inputs.
    *   Pricing Zero-Coupon Bonds, European options on ZCBs, and European Swaptions.
    *   Simulating the `r(t)` path and saving results to a file.
*   **Out of Scope (Handled by Core Engine, potentially AI-assisted):**
    *   Initial data ingestion and validation (may be AI-assisted for anomaly detection).
    *   Construction of the carrier-specific yield curve.
    *   Modeling of dependencies with other risk factors.
    *   Scenario orchestration and final report generation (may be AI-assisted for natural language definition and report generation).

## 2. Conformance to Platform Architecture

*   **FR0.1:** The HW1F plugin **shall** be implemented as a Python class named `HullWhiteOneFactor` that inherits from and correctly implements all methods specified in the `ModelInterface` contract (PAD, Section 5). The `ModelInterface` methods for `calibrate` and `simulate` will now have two forms: a public method that handles file I/O and calls an internal logic method, and an internal logic method that operates purely on in-memory data. While the `ModelInterface` now includes `train` and `predict` methods for Machine Learning models, the HW1F plugin, being a traditional stochastic model, will implement these methods as no-ops or raise a `NotImplementedError` if called, clearly indicating their non-applicability.
*   **FR0.2:** The plugin **shall** be stateless. All state (e.g., calibrated parameters) will be contained within data objects passed to or returned from its methods.
*   **FR0.3 (Revised):** The plugin **shall** handle its own data I/O by reading from and writing to a standardized directory structure. The default root for these operations will be `RiskModels/data/`. This is a deliberate design choice for this specific plugin to allow for easy standalone testing and batch processing.

## 3. Functional Requirements

### 3.1. `ModelInterface` Implementation

*   **FR1.1: `get_name()`**
    *   The method shall return the string `"hull_white_one_factor"`.
*   **FR1.2: `get_required_risk_factors()`**
    *   The method shall return a list of strings representing the market data it needs for calibration, which is `["risk_free_rate_curve", "swaption_volatility_surface"]`.

### 3.2. Calibration (`calibrate` method)

*   **FR2.1: Description:** The `calibrate` method shall find the optimal `a` (mean reversion) and `σ` (volatility) parameters based on market data read from files.
*   **FR2.2: Inputs:**
    *   **Public `calibrate()` method:** This method will have no direct arguments. It **shall** read the following files from the `RiskModels/data/inputs/hull_white_one_factor/` directory:
        *   `initial_zcb_curve.csv`: A CSV file containing maturities and corresponding ZCB prices.
        *   `swaption_volatilities.csv`: A CSV file containing the swaption volatility surface.
    *   **Internal `_calibrate_logic()` method:** This method **shall** take the following arguments:
        *   `initial_zero_coupon_bond_pricer`: A callable function representing the initial zero-coupon bond curve.
        *   `market_swaptions`: A list of dictionaries, each representing a market swaption with its parameters and market price.
*   **FR2.3: Processing:**
    *   The method shall define an objective function that calculates the sum of squared errors between the model's swaption prices and the market swaption prices.
    *   It shall use a numerical optimizer from `scipy.optimize` to find the `a` and `σ` that minimize this error.
    *   The `θ(t)` function shall be determined analytically within the calibration loop to ensure a perfect fit to the provided yield curve for every candidate pair of `(a, σ)`.
*   **FR2.4: Outputs:**
    *   The method shall return a `CalibratedHW1FModel` data object containing:
        *   The calibrated `a*` and `σ*`.
        *   The final, determined `θ(t)` function (or its discrete representation).
        *   The final calibration error (the value from the objective function).

### 3.3. Simulation (`simulate` method)

*   **FR3.1: Description:** The `simulate` method shall generate future paths of the short-term interest rate `r(t)`.
*   **FR3.2: Inputs:**
    *   **Public `simulate()` method:**
        *   `calibrated_model`: The output from the `calibrate` method.
        *   `scenario_definition`: A data object containing simulation parameters (e.g., number of paths, time horizon, time step).
        *   `correlated_shocks` (Optional): A NumPy array of shape `(num_timesteps, num_paths)`. If not provided, the model will generate its own standard normal random variates.
    *   **Internal `_simulate_logic()` method:**
        *   `calibrated_model`: The output from the `calibrate` method.
        *   `scenario_definition`: A data object containing simulation parameters (e.g., number of paths, time horizon, time step).
        *   `correlated_shocks`: A NumPy array of shape `(num_timesteps, num_paths)` containing the standard normal random variates.
*   **FR3.3: Processing:**
    *   The method shall use the provided `correlated_shocks` (or generate its own) to drive the simulation.
    *   The simulation shall be performed using a discretized Euler-Maruyama scheme of the HW1F SDE.
*   **FR3.4: Outputs:**
    *   The method **shall** save the primary simulation results to a CSV file named `simulated_yield_curves.csv` in the `RiskModels/data/outputs/hull_white_one_factor/` directory.
    *   The method **shall** also return a `HW1FSimulationResult` data object containing the simulated paths as a NumPy array for immediate in-memory use.

### 3.4. Pricing (Helper Functions)

*   **FR4.1: Description:** The plugin shall contain internal helper methods to price the derivatives needed for the calibration process. These may be exposed through the plugin's own API for direct pricing use cases.
*   **FR4.2: ZCB Pricer:** A function that takes `(t, T, r_t)` and a `calibrated_model` and returns the price of a Zero-Coupon Bond.
*   **FR4.3: Swaption Pricer:** A function that takes swaption parameters and a `calibrated_model` and returns the price of a European swaption, using Jamshidian's Trick.

## 4. Non-Functional Requirements

*   **NFR1 (Performance):** The calibration process for a typical set of 20 swaptions shall complete in under 30 seconds.
*   **NFR2 (Clarity):** All mathematical formulas shall be linked to their source in academic literature (e.g., Brigo & Mercurio) in the code comments.
*   **NFR3 (Testability):** The code shall be structured to allow for easy unit testing of individual components (e.g., the ZCB pricer, the `B(t,T)` function) in isolation.
