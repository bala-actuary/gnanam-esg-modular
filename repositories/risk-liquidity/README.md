# Liquidity Risk Module

This module provides liquidity risk models for the Gnanam ESG platform, including the Cash Flow Shortfall model for liquidity risk assessment and stress testing.

## 🏗️ Models

### Cash Flow Shortfall Model
- **Location**: `src/models/cash_flow_shortfall_model/`
- **Files**:
  - `model.py` - Core cash flow shortfall model implementation
  - `data_structures.py` - Data structures and types
  - `calculations.py` - Calculation functions and risk metrics
  - `__init__.py` - Module initialization

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### Usage

```python
from src.models.cash_flow_shortfall_model.model import CashFlowShortfallModel

# Create model instance
model = CashFlowShortfallModel()

# Define scenario parameters
scenario_definition = {
    "initial_cash": 1000000,
    "incoming_cash_flows": [50000, 75000, 100000, 125000],
    "outgoing_cash_flows": [80000, 90000, 110000, 95000],
    "time_horizon": 4,  # 4 periods
    "stress_scenarios": ["base", "adverse", "severe"]
}

# Calculate liquidity risk metrics
results = model.calculate_liquidity_risk(scenario_definition)
```

## 🧪 Testing

```bash
# Run all tests
npm run test

# Run unit tests only
npm run test:unit

# Run integration tests
npm run test:integration

# Run with coverage
npm run test:coverage
```

## 📊 API Reference

### CashFlowShortfallModel

#### Methods

- `calculate_liquidity_risk(scenario_definition)` - Calculate liquidity risk metrics
- `simulate_cash_flows(scenario_definition)` - Simulate cash flow scenarios
- `calculate_funding_gap(cash_flows)` - Calculate funding gap
- `stress_test_liquidity(scenarios)` - Perform liquidity stress testing

#### Parameters

- `initial_cash` - Starting cash balance
- `incoming_cash_flows` - Expected incoming cash flows
- `outgoing_cash_flows` - Expected outgoing cash flows
- `time_horizon` - Analysis time horizon
- `stress_scenarios` - Stress scenario definitions

## 📁 Structure

```
risk-liquidity/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── cash_flow_shortfall_model/
│   │       ├── __init__.py
│   │       ├── model.py
│   │       ├── data_structures.py
│   │       └── calculations.py
│   └── index.py
├── tests/
│   └── cash_flow_shortfall_model/
│       ├── test_model.py
│       ├── test_calculations.py
│       └── test_stress_scenarios.py
├── package.json
├── requirements.txt
└── README.md
```

## 🔧 Development

### Adding New Models

1. Create a new directory in `src/models/`
2. Implement the model following the established pattern
3. Add tests in `tests/`
4. Update this README with documentation

### Code Quality

```bash
# Format code
npm run format

# Lint code
npm run lint

# Type checking
mypy src/
```

## 📚 Liquidity Risk Concepts

### Types of Liquidity Risk

1. **Funding Liquidity Risk**
   - Risk of not being able to meet financial obligations
   - Cash flow timing mismatches
   - Funding source availability

2. **Market Liquidity Risk**
   - Risk of not being able to sell assets quickly
   - Bid-ask spread widening
   - Market depth reduction

### Key Metrics

- **Liquidity Coverage Ratio (LCR)**: High-quality liquid assets / Net cash outflows
- **Net Stable Funding Ratio (NSFR)**: Available stable funding / Required stable funding
- **Cash Flow Gap**: Mismatch between inflows and outflows
- **Liquidity Buffer**: Excess liquid assets for stress scenarios

### Stress Scenarios

- **Base Scenario**: Normal market conditions
- **Adverse Scenario**: Moderate stress conditions
- **Severe Scenario**: Extreme stress conditions

## 🏦 Regulatory Framework

The model supports regulatory requirements:
- **Basel III**: LCR and NSFR requirements
- **Dodd-Frank**: Liquidity risk management
- **Solvency II**: Insurance liquidity requirements
- **IFRS 9**: Expected credit loss provisioning

## 📚 References

- Basel Committee on Banking Supervision. (2013). Basel III: The Liquidity Coverage Ratio and liquidity risk monitoring tools.
- European Banking Authority. (2015). Guidelines on liquidity cost benefit allocation.
- Hull, J. C. (2018). Risk management and financial institutions. Wiley.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 