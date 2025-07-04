# RADF Extension Points Documentation

## Overview
This document describes all extension points in the RADF (Risk Aggregation & Dependency Framework) system, enabling developers to add custom functionality without modifying the core codebase.

---

## 1. Aggregation Method Extensions

### Adding Custom Aggregation Methods

**Method 1: Plugin System (Recommended)**
```python
# Create plugins/custom_aggregation.py
def aggregate_custom_method(model_outputs, config):
    """Custom aggregation method implementation."""
    # Your custom logic here
    result = calculate_custom_aggregation(model_outputs, config)
    return {
        'custom_result': result,
        'method': 'custom_method',
        'timestamp': datetime.utcnow().isoformat()
    }
```

**Method 2: Direct Registration**
```python
from RADF.aggregation import register_aggregation_method

def aggregate_my_method(model_outputs, config):
    # Implementation
    return {'result': value}

register_aggregation_method('my_method', aggregate_my_method)
```

### Usage in Config
```yaml
aggregation:
  method: custom_method
  models: [model1, model2]
  custom_param: value
```

---

## 2. Model Extensions

### Adding Custom Models

**Interface Requirements:**
```python
class CustomModel:
    def __init__(self, params):
        self.params = params

    def simulate(self):
        """Run model simulation."""
        # Implementation
        return {
            'risk_measure': [...],
            'paths': [...],
            'metadata': {...}
        }

    def get_name(self):
        return "CustomModel"
```

### Integration Points
- Models can be added to the model registry
- Support for dependency injection
- Custom parameter validation
- Output format standardization

---

## 3. Configuration Extensions

### Custom Config Fields

**Top-Level Extensions:**
```yaml
scenario_name: "Custom Scenario"
models: [...]
aggregation: {...}
# Custom fields
metadata:
  author: "John Doe"
  version: "1.0"
  description: "Custom scenario"
custom_settings:
  optimization_level: "high"
  cache_results: true
```

**Model-Level Extensions:**
```yaml
models:
  - name: CustomModel
    id: custom1
    params:
      standard_param: value
      # Custom parameters
      custom_param1: value1
      custom_param2: value2
    # Custom model metadata
    metadata:
      source: "internal"
      validation_status: "approved"
```

**Aggregation-Level Extensions:**
```yaml
aggregation:
  method: custom_method
  models: [model1, model2]
  # Custom aggregation parameters
  custom_confidence: 0.99
  custom_time_horizon: 2.0
  custom_settings:
    use_parallel: true
    max_iterations: 1000
```

---

## 4. Plugin System Extensions

### Plugin Directory Structure
```
plugins/
├── __init__.py
├── custom_aggregation.py
├── custom_models.py
├── custom_validators.py
└── custom_exporters.py
```

### Plugin Loading
```python
from RADF.aggregation import load_aggregation_plugins
from RADF.orchestrator import RADFOrchestrator

# Load plugins before running scenarios
load_aggregation_plugins('plugins')

# Run scenario with custom methods
orchestrator = RADFOrchestrator('scenario.yaml')
orchestrator.run()
```

---

## 5. Validation Extensions

### Custom Validators
```python
def validate_custom_field(config, field_name):
    """Custom validation for specific fields."""
    if field_name in config:
        value = config[field_name]
        # Custom validation logic
        if not is_valid_custom_value(value):
            raise ValueError(f"Invalid {field_name}: {value}")
    return True

# Register custom validator
CUSTOM_VALIDATORS = {
    'custom_field': validate_custom_field
}
```

---

## 6. Export Extensions

### Custom Export Formats
```python
def export_custom_format(audit_log, config):
    """Export audit log in custom format."""
    # Custom export logic
    return custom_formatted_output

# Register custom exporter
CUSTOM_EXPORTERS = {
    'custom_format': export_custom_format
}
```

---

## 7. Error Handling Extensions

### Custom Error Types
```python
class CustomRADFError(RADFError):
    """Custom error type for specific functionality."""
    pass

class ValidationError(CustomRADFError):
    """Custom validation error."""
    pass
```

---

## 8. Logging Extensions

### Custom Audit Events
```python
def log_custom_event(orchestrator, event_type, details):
    """Log custom audit events."""
    orchestrator._log_audit_event(
        event_type,
        details,
        status="success"
    )
```

---

## 9. Testing Extensions

### Custom Test Scenarios
```python
def create_custom_test_scenario():
    """Create custom test scenario for validation."""
    return {
        "scenario_name": "Custom Test",
        "models": [...],
        "aggregation": {...},
        "expected_results": {...}
    }
```

---

## 10. Best Practices

### Code Organization
- Keep custom code in dedicated modules
- Use clear naming conventions
- Document all custom functionality
- Include unit tests for custom code

### Error Handling
- Always validate custom inputs
- Provide meaningful error messages
- Handle edge cases gracefully
- Log custom operations for audit trails

### Performance
- Optimize custom aggregation methods
- Use efficient data structures
- Consider parallel processing for large datasets
- Cache results when appropriate

### Security
- Validate all custom inputs
- Sanitize user-provided data
- Use secure default values
- Implement proper access controls

---

## 11. Examples

### Complete Custom Aggregation Plugin
```python
# plugins/advanced_copula.py
import numpy as np
from scipy.stats import norm

def aggregate_advanced_copula(model_outputs, config):
    """Advanced copula-based aggregation method."""
    # Extract parameters
    confidence_level = config.get('confidence_level', 0.99)
    correlation_matrix = config.get('correlation_matrix', None)

    # Implementation
    # ... copula calculation logic ...

    return {
        'copula_result': result,
        'confidence_level': confidence_level,
        'method': 'advanced_copula',
        'correlation_matrix': correlation_matrix
    }
```

### Custom Model Plugin
```python
# plugins/custom_risk_model.py
class CustomRiskModel:
    def __init__(self, params):
        self.params = params
        self.validate_params()

    def validate_params(self):
        """Validate model parameters."""
        required = ['volatility', 'drift', 'time_horizon']
        for param in required:
            if param not in self.params:
                raise ValueError(f"Missing required parameter: {param}")

    def simulate(self):
        """Run Monte Carlo simulation."""
        # Implementation
        return {
            'risk_measure': simulated_values,
            'paths': simulation_paths,
            'metadata': {
                'model_type': 'custom_risk',
                'parameters': self.params
            }
        }
```

---

## 12. Integration Guidelines

### Version Compatibility
- Test custom extensions with different RADF versions
- Use version-specific APIs when available
- Maintain backward compatibility when possible

### Documentation
- Document all custom extensions
- Provide usage examples
- Include parameter descriptions
- Document error conditions

### Testing
- Write unit tests for custom code
- Include integration tests
- Test edge cases and error conditions
- Validate performance characteristics

---

This documentation provides a comprehensive guide for extending the RADF system while maintaining code quality, performance, and security standards.
