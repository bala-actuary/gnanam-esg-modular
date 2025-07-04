# Equity Risk Module

This module provides equity risk models for the Gnanam ESG platform, including the Geometric Brownian Motion (GBM) model for equity price simulation and risk assessment.

## 🏗️ Models

### Geometric Brownian Motion (GBM) Model
- **Location**: `src/models/gbm_model/`
- **Files**:
  - `model.py` - Core GBM model implementation
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
from src.models.gbm_model.model import GBMModel

# Create model instance
model = GBMModel()

# Set parameters
model.set_parameters(
    initial_price=100.0,
    drift=0.05,
    volatility=0.20,
    time_steps=252,
    num_paths=1000
)

# Simulate price paths
paths = model.simulate()

# Calculate risk metrics
var_95 = model.calculate_value_at_risk(confidence_level=0.95)
expected_shortfall = model.calculate_expected_shortfall(confidence_level=0.95)
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

### GBMModel

#### Methods

- `set_parameters(initial_price, drift, volatility, time_steps, num_paths)` - Set model parameters
- `simulate()` - Generate price paths using GBM
- `calculate_value_at_risk(confidence_level)` - Calculate VaR
- `calculate_expected_shortfall(confidence_level)` - Calculate Expected Shortfall
- `calculate_volatility()` - Calculate realized volatility
- `plot_paths()` - Visualize simulated paths

#### Parameters

- `initial_price` - Starting price of the equity
- `drift` - Expected return (annualized)
- `volatility` - Price volatility (annualized)
- `time_steps` - Number of time steps for simulation
- `num_paths` - Number of simulation paths

## 📁 Structure

```
risk-equity/
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
│       └── test_risk_metrics.py
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

### Geometric Brownian Motion

The GBM model assumes that the price of an equity follows:

```
dS(t) = μS(t)dt + σS(t)dW(t)
```

Where:
- S(t) is the price at time t
- μ is the drift (expected return)
- σ is the volatility
- W(t) is a Wiener process

The solution is:
```
S(t) = S(0) * exp((μ - 0.5σ²)t + σW(t))
```

### Risk Metrics

- **Value at Risk (VaR)**: Maximum expected loss at a given confidence level
- **Expected Shortfall**: Average loss beyond the VaR threshold
- **Volatility**: Standard deviation of returns

## 📚 References

- Hull, J. C. (2018). Options, futures, and other derivatives. Pearson.
- Glasserman, P. (2013). Monte Carlo methods in financial engineering. Springer.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 