# Software Requirements Specification (SRS)
### Model Plugin: Basic Exposure Model for Counterparty Risk
**Version:** 1.0
**Date:** 28 June 2025

## 1. Introduction

#### 1.1 Purpose
This document specifies the software requirements for the **Basic Exposure Model Plugin** within the "RiskModels" platform. It details the functional and non-functional requirements necessary for the model's implementation and calculation capabilities for counterparty exposure.

#### 1.2 Scope
This SRS covers the Basic Exposure Model's core functionality, including its ability to calculate the exposure to a counterparty based on the current market value of a portfolio of trades. It will integrate with the platform's data access layer for input and output, and leverage the visualization module for graphical representation of results.

## 2. Functional Requirements

#### 2.1. Model Calculation
*   **FR1.1 - Input Data:** The model shall accept as input:
    *   A portfolio of trades with current market values (positive for assets, negative for liabilities).
    *   Counterparty identifier for each trade.
*   **FR1.2 - Calculation Output:** The model shall calculate and output:
    *   Total current exposure for each counterparty (sum of market values of trades with that counterparty).
    *   Positive exposure for each counterparty (sum of positive market values).
    *   Negative exposure for each counterparty (sum of negative market values).

#### 2.2. Data Handling
*   **FR2.1 - Hybrid I/O:** The model shall support both file-based (CSV) and in-memory data handling for inputs and outputs.
*   **FR2.2 - Input File Format:** The model shall expect input data in a predefined CSV format (e.g., `trades_portfolio.csv` with columns for `Counterparty_ID`, `Trade_ID`, `Market_Value`).
*   **FR2.3 - Output File Format:** The model shall output calculated results (e.g., total exposure, positive exposure, negative exposure per counterparty) to CSV files with clear, labeled columns.

#### 2.3. Visualization
*   **FR3.1 - Graphical Output:** The model shall generate interactive plots (e.g., bar chart of exposures per counterparty) using the platform's visualization module. Users shall be able to configure which plots are generated.

## 3. Non-Functional Requirements

#### 3.1. Performance
*   **NFR3.1.1 - Calculation Speed:** Calculation of exposures should be efficient for typical portfolio sizes.

#### 3.2. Accuracy
*   **NFR3.2.1 - Calculation Accuracy:** All calculations shall adhere to standard financial principles for exposure aggregation.
*   **NFR3.2.2 - Validation:** The model's outputs shall be validated against manually calculated examples or benchmark data where available.

#### 3.3. Usability
*   **NFR3.3.1 - Clear Interface:** The model's public interface shall be intuitive and consistent with the `ModelInterface` contract.
*   **NFR3.3.2 - Documentation:** Comprehensive internal and external documentation shall be provided.

#### 3.4. Maintainability
*   **NFR3.4.1 - Modularity:** The codebase shall be modular, with clear separation of concerns (e.g., data processing, calculation logic).
*   **NFR3.4.2 - Testability:** All components shall be unit-testable.

#### 3.5. Security
*   **NFR3.5.1 - Data Security:** The model shall not expose sensitive data or introduce vulnerabilities.

## 4. Constraints

*   **C4.1 - Programming Language:** Python.
*   **C4.2 - Core Engine Integration:** Must adhere to the `ModelInterface` contract.
*   **C4.3 - Data Formats:** CSV for file-based I/O.

## 5. Future Considerations

*   Extension to include Potential Future Exposure (PFE) calculations.
*   Incorporation of netting agreements and collateral.
*   Advanced visualization options for exposure profiles.
