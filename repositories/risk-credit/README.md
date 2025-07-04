# Credit Risk Module

This module provides credit risk models for the Gnanam ESG platform, including the Merton structural model for default probability estimation.

## 🏗️ Models

### Merton Structural Model
- **Location**: `src/models/merton_model/`
- **Files**:
  - `model.py` - Core model implementation
  - `data_structures.py` - Data structures and types
  - `formulas.py` - Mathematical formulas
  - `calculations.py` - Calculation functions

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
from src.models.merton_model.model import MertonModel

# Create model instance
model = MertonModel()

# Set parameters
model.set_parameters(
    asset_value=1000000,
    debt_value=800000,
    asset_volatility=0.25,
    risk_free_rate=0.05,
    time_to_maturity=1.0
)

# Calculate default probability
default_prob = model.calculate_default_probability()

# Calculate distance to default
distance_to_default = model.calculate_distance_to_default()
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

### MertonModel

#### Methods

- `set_parameters(asset_value, debt_value, asset_volatility, risk_free_rate, time_to_maturity)` - Set model parameters
- `calculate_default_probability()` - Calculate probability of default
- `calculate_distance_to_default()` - Calculate distance to default
- `calculate_credit_spread()` - Calculate credit spread
- `calibrate(market_data)` - Calibrate to market data

#### Parameters

- `asset_value` - Current value of firm's assets
- `debt_value` - Face value of debt
- `asset_volatility` - Volatility of asset returns
- `risk_free_rate` - Risk-free interest rate
- `time_to_maturity` - Time to debt maturity

## 📁 Structure

```
risk-credit/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── merton_model/
│   │       ├── __init__.py
│   │       ├── model.py
│   │       ├── data_structures.py
│   │       ├── formulas.py
│   │       └── calculations.py
│   └── index.py
├── tests/
│   └── merton_model/
│       ├── test_model.py
│       ├── test_calculations.py
│       └── test_calibration.py
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

## 📚 References

- Merton, R. C. (1974). On the pricing of corporate debt: The risk structure of interest rates. The Journal of Finance, 29(2), 449-470.
- Hull, J. C. (2018). Options, futures, and other derivatives. Pearson.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 