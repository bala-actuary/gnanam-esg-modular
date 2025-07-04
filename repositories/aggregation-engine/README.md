# Aggregation Engine Module

This module provides the Risk Aggregation and Distribution Framework (RADF) for the Gnanam ESG platform, enabling comprehensive multi-risk scenario aggregation and portfolio risk analysis.

## 🏗️ Architecture

### Core Components
- **RADF Orchestrator**: Central coordination and workflow management
- **Risk Model Integration**: Seamless integration with all risk modules
- **Scenario Aggregation**: Multi-risk scenario combination and analysis
- **Plugin System**: Extensible architecture for custom risk models
- **Performance Monitoring**: Real-time aggregation performance tracking

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### Development

```bash
# Start aggregation engine
npm run dev

# Or directly with Python
python src/__main__.py --dev
```

### Testing

```bash
# Run test harness
npm run harness

# Run all tests
npm run test

# Run unit tests only
npm run test:unit

# Run integration tests
npm run test:integration
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

# Run test harness
npm run harness
```

## 📊 API Reference

### RADF Orchestrator

#### Methods

- `aggregate_scenario(scenario_definition)` - Aggregate multiple risk scenarios
- `distribute_risk(portfolio_data)` - Distribute risk across portfolio
- `run_workflow(workflow_config)` - Execute complete risk workflow
- `get_aggregation_results(scenario_id)` - Retrieve aggregation results

#### Parameters

- `scenario_definition` - Multi-risk scenario configuration
- `portfolio_data` - Portfolio composition and weights
- `workflow_config` - Complete workflow configuration
- `scenario_id` - Unique scenario identifier

## 📁 Structure

```
aggregation-engine/
├── src/
│   ├── __main__.py           # Main entry point
│   ├── __init__.py           # Module initialization
│   ├── config.py             # Configuration management
│   ├── orchestrator.py       # RADF orchestrator
│   ├── aggregation.py        # Core aggregation logic
│   ├── test_harness.py       # Test harness
│   └── plugins/              # Plugin system
│       ├── __init__.py
│       └── demo_plugin.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── package.json
├── requirements.txt
└── README.md
```

## 🔧 Development

### Adding New Plugins

1. Create plugin file in `src/plugins/`
2. Implement required interface methods
3. Register plugin in orchestrator
4. Add tests in `tests/`

### Configuration

Environment variables:
```bash
# Aggregation Settings
AGGREGATION_METHOD=monte_carlo
CORRELATION_MATRIX_PATH=/path/to/correlation.csv
CONFIDENCE_LEVEL=0.99

# Performance
MAX_WORKERS=4
CHUNK_SIZE=1000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Code Quality

```bash
# Format code
npm run format

# Lint code
npm run lint

# Type checking
mypy src/
```

## 📚 Aggregation Concepts

### Risk Aggregation Methods

1. **Monte Carlo Simulation**
   - Stochastic scenario generation
   - Correlation matrix integration
   - Confidence interval calculation

2. **Analytical Methods**
   - Variance-covariance approach
   - Copula-based aggregation
   - Stress testing integration

3. **Historical Simulation**
   - Historical scenario analysis
   - Bootstrap resampling
   - Extreme value theory

### Portfolio Risk Metrics

- **Value at Risk (VaR)**: Maximum expected loss at confidence level
- **Expected Shortfall (ES)**: Average loss beyond VaR
- **Portfolio Volatility**: Standard deviation of portfolio returns
- **Risk Contribution**: Individual asset risk contribution
- **Diversification Ratio**: Portfolio diversification measure

### Correlation Handling

- **Historical Correlation**: Based on historical data
- **Stress Correlation**: Under stress scenarios
- **Dynamic Correlation**: Time-varying correlations
- **Copula Models**: Flexible dependency structures

## 🔄 Integration

### Risk Model Communication

- **Synchronous Calls**: Direct API calls to risk modules
- **Asynchronous Processing**: Queue-based processing
- **Batch Processing**: Bulk scenario processing
- **Real-time Streaming**: Live risk updates

### External Services

- **API Gateway**: Request routing and authentication
- **Risk Modules**: Individual risk model services
- **Monitoring Dashboard**: Real-time aggregation monitoring
- **Data Services**: Market data and reference data

## 📈 Performance Optimization

### Parallel Processing

- **Multi-threading**: CPU-intensive calculations
- **Multi-processing**: Memory-intensive operations
- **Distributed Computing**: Cluster-based processing
- **GPU Acceleration**: CUDA-based calculations

### Caching Strategy

- **Result Caching**: Store aggregation results
- **Model Caching**: Cache risk model outputs
- **Configuration Caching**: Cache workflow configurations
- **Distributed Caching**: Redis-based caching

## 🚀 Deployment

### Docker
```bash
# Build image
docker build -t gnanam/aggregation-engine .

# Run container
docker run -p 8002:8002 gnanam/aggregation-engine
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aggregation-engine
spec:
  replicas: 2
  selector:
    matchLabels:
      app: aggregation-engine
  template:
    metadata:
      labels:
        app: aggregation-engine
    spec:
      containers:
      - name: aggregation-engine
        image: gnanam/aggregation-engine:latest
        ports:
        - containerPort: 8002
```

## 📚 References

- Jorion, P. (2007). Value at Risk: The New Benchmark for Managing Financial Risk.
- McNeil, A. J., Frey, R., & Embrechts, P. (2015). Quantitative Risk Management.
- Hull, J. C. (2018). Risk Management and Financial Institutions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 