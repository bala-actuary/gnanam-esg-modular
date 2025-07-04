# Counterparty Risk Module

This module provides counterparty risk models for the Gnanam ESG platform, including the Basic Exposure Model for counterparty credit risk assessment and exposure calculation.

## 🏗️ Models

### Basic Exposure Model
- **Location**: `src/models/basic_exposure_model/`
- **Files**:
  - `model.py` - Core basic exposure model implementation
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
from src.models.basic_exposure_model.model import BasicExposureModel

# Create model instance
model = BasicExposureModel()

# Define scenario parameters
scenario_definition = {
    "counterparty_id": "CP001",
    "exposure_amount": 1000000,
    "default_probability": 0.02,
    "recovery_rate": 0.40,
    "time_horizon": 1.0,
    "confidence_level": 0.99
}

# Calculate counterparty risk metrics
results = model.calculate_exposure(scenario_definition)
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

### BasicExposureModel

#### Methods

- `calculate_exposure(scenario_definition)` - Calculate counterparty exposure
- `calculate_expected_loss(exposure, pd, lgd)` - Calculate expected loss
- `calculate_potential_future_exposure(scenarios)` - Calculate PFE
- `stress_test_counterparty(scenarios)` - Perform stress testing

#### Parameters

- `counterparty_id` - Unique identifier for the counterparty
- `exposure_amount` - Current exposure amount
- `default_probability` - Probability of default (PD)
- `recovery_rate` - Recovery rate in case of default
- `time_horizon` - Analysis time horizon
- `confidence_level` - Confidence level for risk metrics

## 📁 Structure

```
risk-counterparty/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── basic_exposure_model/
│   │       ├── __init__.py
│   │       ├── model.py
│   │       ├── data_structures.py
│   │       └── calculations.py
│   └── index.py
├── tests/
│   └── basic_exposure_model/
│       ├── test_model.py
│       ├── test_calculations.py
│       └── test_exposure_metrics.py
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

## 📚 Counterparty Risk Concepts

### Types of Counterparty Risk

1. **Pre-Settlement Risk**
   - Risk of counterparty default before settlement
   - Current exposure to the counterparty
   - Potential future exposure (PFE)

2. **Settlement Risk**
   - Risk during the settlement process
   - Herstatt risk (time zone differences)
   - Delivery vs. payment risk

### Key Metrics

- **Current Exposure**: Current mark-to-market value
- **Potential Future Exposure (PFE)**: Maximum expected exposure at a confidence level
- **Expected Positive Exposure (EPE)**: Average of positive exposures
- **Expected Loss (EL)**: PD × LGD × EAD
- **Credit Value Adjustment (CVA)**: Market value of counterparty credit risk

### Risk Components

- **Probability of Default (PD)**: Likelihood of counterparty default
- **Loss Given Default (LGD)**: Loss in case of default (1 - Recovery Rate)
- **Exposure at Default (EAD)**: Exposure at the time of default

## 🏦 Regulatory Framework

The model supports regulatory requirements:
- **Basel III**: Credit risk capital requirements
- **IFRS 9**: Expected credit loss provisioning
- **CVA Capital**: Credit value adjustment capital
- **CCR**: Counterparty Credit Risk framework

## 📚 References

- Basel Committee on Banking Supervision. (2014). The standardised approach for measuring counterparty credit risk exposures.
- International Accounting Standards Board. (2014). IFRS 9 Financial Instruments.
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