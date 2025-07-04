# RADF Aggregation Engine — Detailed Design (Updated)

## Purpose
The aggregation engine combines outputs from multiple models into portfolio-level risk measures. It supports a registry of aggregation methods, handles different time grids/paths, and is designed for extensibility and market-leading flexibility.

---

## 1. Interface
- Aggregation engine exposes a main function:
  - `aggregate(results: dict, config: dict) -> dict`
    - `results`: Dictionary of model outputs (keyed by model id)
    - `config`: Aggregation config section from scenario file
    - Returns: Aggregated results (dict, JSON, or CSV)
- New methods can be registered via `register_aggregation_method(name, func)` or by adding a plugin.

---

## 2. Registry of Aggregation Methods
- Aggregation methods are registered in a central registry (dict or plugin system)
- Each method implements a function:
  - `def aggregate_<method>(model_outputs: dict, config: dict) -> dict`
- Supported out of the box (scaffolded):
  - `sum`: Simple sum of risk measures
  - `VaR`: Value-at-Risk at specified confidence level
  - `ES`: Expected Shortfall at specified confidence level
  - `gaussian_copula`: Gaussian copula aggregation
  - `t_copula`: t-copula aggregation
  - `archimedean_copula`: Archimedean copula aggregation
  - `scenario_based`: Scenario-based aggregation
  - `stress`: Stress aggregation
  - `tail_risk`: Tail risk aggregation
  - `correlation`: Correlation-based aggregation
- New methods can be added by registering a function or via plugins.

---

## 3. Handling Different Time Grids/Paths
- Aligns time grids across models (interpolation if needed)
- Handles different numbers of simulation paths (resampling or truncation)
- Ensures aggregation is performed on compatible data structures

---

## 4. Extensibility
- New aggregation methods can be added by registering a new function:
  ```python
  from aggregation import register_aggregation_method
  def aggregate_custom(model_outputs, config):
      # ...
      return {...}
  register_aggregation_method('custom', aggregate_custom)
  ```
- Methods can be loaded dynamically from plugins (see below)
- Config schema allows for method-specific parameters

---

## 5. How to Add an Aggregation Plugin

You can add new aggregation methods without modifying the core code by creating a plugin:

1. **Create a Python file in the `plugins/` directory** (e.g., `plugins/my_plugin.py`).
2. **Define a function named `aggregate_<method>`** (e.g., `aggregate_myagg`).
   - The function must accept `(model_outputs, config)` as arguments and return a dict.
3. **(Optional) Add a docstring** to describe your method.
4. **Call `load_aggregation_plugins('plugins')`** before running aggregation (the orchestrator can do this automatically).
5. **Use your method in the scenario config:**
   ```yaml
   aggregation:
     method: myagg
     ...
   ```

**Example plugin (`plugins/demo_plugin.py`):**
```python
"""
Demo aggregation plugin for RADF.
This function will be auto-registered if the plugin loader is called.
"""
def aggregate_demo(model_outputs, config):
    """Demo aggregation method: returns the number of models and a static value."""
    return {
        'demo': True,
        'num_models': len(model_outputs),
        'static_value': 42
    }
```

---

## 6. Example Usage
```python
from aggregation import aggregate, load_aggregation_plugins
load_aggregation_plugins('plugins')
results = {
    'hw1f': {'risk_measure': [0.1, 0.2, 0.3]},
    'merton': {'risk_measure': [0.05, 0.15, 0.25]},
}
config = {
    'method': 'demo',
    'models': ['hw1f', 'merton']
}
agg_result = aggregate(results, config)
```

---

## 7. Output
- Aggregated results are returned as a dict (or can be exported as JSON/CSV)
- Example:
```json
{
  "demo": true,
  "num_models": 2,
  "static_value": 42
}
```

---

## 8. Review Checklist
- [ ] Is the interface clear and easy to use?
- [ ] Is the registry/extensibility approach robust?
- [ ] Are time grid/path alignment strategies sufficient?
- [ ] Are example usages and outputs clear?
- [ ] Are all major market aggregation methods scaffolded?
- [ ] Is plugin usage and extension clearly documented?

---
