# Inflation Risk Module

This module provides inflation risk models for the Gnanam ESG platform, including the Mean Reverting (Ornstein-Uhlenbeck) model for inflation rate simulation and risk assessment.

## 🏗️ Models

### Mean Reverting Model (Ornstein-Uhlenbeck Process)
- **Location**: `src/models/mean_reverting_model/`
- **Files**:
  - `model.py` - Core mean reverting model implementation
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
from src.models.mean_reverting_model.model import MeanRevertingModel

# Create model instance
model = MeanRevertingModel()

# Define scenario parameters
scenario_definition = {
    "initial_inflation_rate": 0.025,  # 2.5% initial inflation
    "long_term_mean": 0.02,           # 2% long-term target
    "mean_reversion_speed": 0.1,      # Speed of mean reversion
    "volatility": 0.05,               # Inflation volatility
    "time_horizon": 10.0,             # 10-year horizon
    "num_time_steps": 120,            # Monthly steps
    "num_paths": 1000
}

# Simulate inflation rate paths
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

### MeanRevertingModel

#### Methods

- `simulate(scenario_definition, correlated_shocks=None, plot_options=None)` - Generate inflation rate paths
- `get_name()` - Return model name
- `get_required_risk_factors()` - Return required risk factors

#### Parameters

- `initial_inflation_rate` - Starting inflation rate
- `long_term_mean` - Long-term mean inflation rate
- `mean_reversion_speed` - Speed of mean reversion (kappa)
- `volatility` - Inflation rate volatility
- `time_horizon` - Simulation time horizon
- `num_time_steps` - Number of time steps for simulation
- `num_paths` - Number of simulation paths

## 📁 Structure

```
risk-inflation/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── mean_reverting_model/
│   │       ├── __init__.py
│   │       ├── model.py
│   │       ├── data_structures.py
│   │       └── formulas.py
│   └── index.py
├── tests/
│   └── mean_reverting_model/
│       ├── test_model.py
│       ├── test_simulation.py
│       └── test_inflation_metrics.py
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

### Ornstein-Uhlenbeck Process

The mean reverting model assumes that inflation follows an Ornstein-Uhlenbeck process:

```
dπ(t) = κ(θ - π(t))dt + σdW(t)
```

Where:
- π(t) is the inflation rate at time t
- κ is the mean reversion speed (positive)
- θ is the long-term mean inflation rate
- σ is the volatility
- W(t) is a Wiener process

The solution is:
```
π(t) = θ + (π(0) - θ)e^(-κt) + σ∫₀ᵗ e^(-κ(t-s))dW(s)
```

### Mean Reversion Properties

- **Mean Reversion**: Inflation tends to revert to its long-term mean
- **Stationarity**: The process is stationary when κ > 0
- **Volatility**: Short-term volatility with long-term stability
- **Central Bank Target**: θ can represent central bank inflation targets

### Inflation Risk Metrics

- **Inflation Volatility**: Standard deviation of inflation rate changes
- **Inflation Duration**: Time to revert to long-term mean
- **Inflation Risk Premium**: Compensation for inflation uncertainty
- **Real Rate Risk**: Impact on real interest rates

## 🏦 Central Bank Integration

The model can be calibrated to central bank targets:
- **Federal Reserve**: 2% long-term target
- **European Central Bank**: 2% symmetric target
- **Bank of England**: 2% target
- **Bank of Japan**: 2% target

## 📚 References

- Vasicek, O. (1977). An equilibrium characterization of the term structure. Journal of Financial Economics, 5(2), 177-188.
- Hull, J. C. (2018). Options, futures, and other derivatives. Pearson.
- Brigo, D., & Mercurio, F. (2006). Interest rate models: Theory and practice. Springer.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 