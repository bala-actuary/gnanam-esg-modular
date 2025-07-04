# Interest Rate Risk Module

This module provides interest rate risk models for the Gnanam ESG platform, including the Hull-White one-factor model and related pricing and calibration tools.

## 🏗️ Models

### Hull-White One-Factor Model
- **Location**: `src/models/hull_white_one_factor/`
- **Files**:
  - `model.py` - Core model implementation
  - `data_structures.py` - Data structures and types
  - `formulas.py` - Mathematical formulas
  - `pricing.py` - Pricing functions

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
from src.models.hull_white_one_factor.model import HullWhiteOneFactorModel

# Create model instance
model = HullWhiteOneFactorModel()

# Set parameters
model.set_parameters(alpha=0.1, sigma=0.02)

# Price a zero-coupon bond
price = model.price_zero_coupon_bond(face_value=100, maturity=5)
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

### HullWhiteOneFactorModel

#### Methods

- `set_parameters(alpha, sigma)` - Set model parameters
- `price_zero_coupon_bond(face_value, maturity)` - Price zero-coupon bonds
- `calibrate(market_data)` - Calibrate to market data
- `simulate_paths(time_steps, num_paths)` - Simulate interest rate paths

#### Parameters

- `alpha` - Mean reversion speed
- `sigma` - Volatility parameter

## 📁 Structure

```
risk-interest-rate/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── hull_white_one_factor/
│   │       ├── __init__.py
│   │       ├── model.py
│   │       ├── data_structures.py
│   │       ├── formulas.py
│   │       └── pricing.py
│   └── index.py
├── tests/
│   └── hull_white_one_factor/
│       ├── test_model.py
│       ├── test_pricing.py
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

- Hull, J., & White, A. (1990). Pricing interest-rate-derivative securities. The Review of Financial Studies, 3(4), 573-592.
- Brigo, D., & Mercurio, F. (2006). Interest rate models: theory and practice. Springer Science & Business Media.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 