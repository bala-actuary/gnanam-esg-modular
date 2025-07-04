# Foreign Exchange Risk Module

This module provides foreign exchange risk models for the Gnanam ESG platform, including the Geometric Brownian Motion (GBM) model for currency pair simulation and FX risk assessment.

## 🏗️ Models

### FX Geometric Brownian Motion (GBM) Model
- **Location**: `src/models/gbm_model/`
- **Files**:
  - `model.py` - Core FX GBM model implementation
  - `data_structures.py` - Data structures and types
  - `formulas.py` - Mathematical formulas and calculations
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
from src.models.gbm_model.model import FXGBMModel

# Create model instance
model = FXGBMModel()

# Define scenario parameters
scenario_definition = {
    "initial_rate": 1.2000,  # EUR/USD exchange rate
    "expected_return": 0.02,
    "volatility": 0.15,
    "time_horizon": 1.0,
    "num_time_steps": 252,
    "num_paths": 1000
}

# Simulate exchange rate paths
simulation_result = model.simulate(scenario_definition)
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

### FXGBMModel

#### Methods

- `simulate(scenario_definition, correlated_shocks=None, plot_options=None)` - Generate FX rate paths
- `get_name()` - Return model name
- `get_required_risk_factors()` - Return required risk factors

#### Parameters

- `initial_rate` - Starting exchange rate
- `expected_return` - Expected return (annualized)
- `volatility` - Exchange rate volatility (annualized)
- `time_horizon` - Simulation time horizon
- `num_time_steps` - Number of time steps for simulation
- `num_paths` - Number of simulation paths

## 📁 Structure

```
risk-foreign-exchange/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── gbm_model/
│   │       ├── __init__.py
│   │       ├── model.py
│   │       ├── data_structures.py
│   │       └── formulas.py
│   └── index.py
├── tests/
│   └── gbm_model/
│       ├── test_model.py
│       ├── test_simulation.py
│       └── test_fx_metrics.py
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

## 📚 Mathematical Background

### FX Geometric Brownian Motion

The FX GBM model assumes that the exchange rate follows:

```
dS(t) = μS(t)dt + σS(t)dW(t)
```

Where:
- S(t) is the exchange rate at time t
- μ is the drift (expected return)
- σ is the volatility
- W(t) is a Wiener process

The solution is:
```
S(t) = S(0) * exp((μ - 0.5σ²)t + σW(t))
```

### FX Risk Metrics

- **Exchange Rate Volatility**: Standard deviation of exchange rate changes
- **Value at Risk (VaR)**: Maximum expected loss due to FX movements
- **Expected Shortfall**: Average loss beyond the VaR threshold
- **Currency Exposure**: Sensitivity to exchange rate changes

## 🌍 Currency Pairs

The model supports simulation of various currency pairs:
- EUR/USD (Euro/US Dollar)
- GBP/USD (British Pound/US Dollar)
- USD/JPY (US Dollar/Japanese Yen)
- USD/CHF (US Dollar/Swiss Franc)
- And other major currency pairs

## 📚 References

- Hull, J. C. (2018). Options, futures, and other derivatives. Pearson.
- Glasserman, P. (2013). Monte Carlo methods in financial engineering. Springer.
- Garman, M. B., & Kohlhagen, S. W. (1983). Foreign currency option values. Journal of International Money and Finance, 2(3), 231-237.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 