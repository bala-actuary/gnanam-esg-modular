# Integration Testing Framework

## Overview

The Integration Testing Framework for the Gnanam ESG Modular Platform provides comprehensive testing capabilities to validate that all modules work together properly in the modular architecture.

## Features

- **Unit Testing**: Individual module functionality validation
- **Workflow Testing**: End-to-end workflow integration testing
- **Performance Testing**: Performance and scalability validation
- **API Testing**: API endpoint and integration testing
- **Automated Reporting**: Detailed test results and summaries
- **Configurable Test Suites**: Flexible test configuration via JSON

## Directory Structure

```
integration-tests/
├── test_framework.py      # Main testing framework
├── run_tests.py          # Test runner script
├── test_config.json      # Test configuration
├── requirements.txt      # Dependencies
├── README.md            # This file
├── unit/                # Unit test specific files
├── workflow/            # Workflow test specific files
├── performance/         # Performance test specific files
└── api/                 # API test specific files
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run All Tests

```bash
python run_tests.py
```

### 3. Run Specific Test Types

```bash
# Unit tests only
python run_tests.py --test-type unit

# Workflow tests only
python run_tests.py --test-type workflow

# Performance tests only
python run_tests.py --test-type performance

# API tests only
python run_tests.py --test-type api
```

### 4. Run with Verbose Output

```bash
python run_tests.py --verbose
```

## Test Types

### Unit Tests

Tests individual module functionality:

- **Module Structure**: Validates file structure and configuration
- **Module Imports**: Tests module imports and dependencies
- **Risk Model Functionality**: Tests specific risk model calculations

**Example Output:**
```
🧪 Running unit tests...
==================================================

📊 Unit Test Summary:
Total Tests: 36
Passed: 36
Failed: 0
Success Rate: 100.0%
Total Duration: 2.45s

✅ All unit tests passed!
```

### Workflow Tests

Tests end-to-end workflow integration:

- **Risk Analysis Workflow**: Complete risk analysis pipeline
- **Data Processing Workflow**: Data preprocessing and validation
- **AI Analysis Workflow**: AI integration and insights generation

**Example Output:**
```
🧪 Running workflow tests...
==================================================

📊 Workflow Test Summary:
Total Tests: 1
Passed: 1
Failed: 0
Success Rate: 100.0%
Total Duration: 1.23s

✅ All workflow tests passed!
```

### Performance Tests

Tests performance and scalability:

- **Module Performance**: Individual module performance metrics
- **System Scalability**: System-wide scalability testing
- **Resource Usage**: Memory and CPU usage monitoring

**Example Output:**
```
🧪 Running performance tests...
==================================================

📊 Performance Test Summary:
Total Tests: 13
Passed: 13
Failed: 0
Success Rate: 100.0%
Total Duration: 3.67s

✅ All performance tests passed!
```

### API Tests

Tests API integration and endpoints:

- **Health Checks**: Service health endpoint validation
- **Model Endpoints**: Risk model API endpoints
- **Integration Endpoints**: Cross-module API integration

**Example Output:**
```
🧪 Running api tests...
==================================================

📊 API Test Summary:
Total Tests: 3
Passed: 3
Failed: 0
Success Rate: 100.0%
Total Duration: 0.89s

✅ All api tests passed!
```

## Test Configuration

The `test_config.json` file contains comprehensive test configuration:

### Test Suites

```json
{
  "test_suites": {
    "unit_tests": {
      "name": "Unit Tests",
      "description": "Individual module functionality tests",
      "timeout": 300,
      "parallel": true,
      "modules": ["risk-interest-rate", "risk-credit", ...]
    }
  }
}
```

### Module Configurations

```json
{
  "module_configs": {
    "risk-interest-rate": {
      "test_parameters": {
        "alpha": 0.1,
        "sigma": 0.02,
        "initial_rate": 0.05
      },
      "expected_outputs": {
        "rate_path": "array",
        "volatility": "float"
      }
    }
  }
}
```

### Performance Benchmarks

```json
{
  "performance_benchmarks": {
    "single_model_execution": {
      "max_duration": 5.0,
      "max_memory": 512,
      "max_cpu": 50.0
    }
  }
}
```

## Test Results

### JSON Results

Test results are saved to `test_results.json`:

```json
{
  "summary": {
    "total_tests": 53,
    "passed": 53,
    "failed": 0,
    "success_rate": 100.0,
    "total_duration": 8.24
  },
  "results": [
    {
      "test_id": "risk-interest-rate_structure",
      "test_name": "Module Structure Test",
      "test_type": "unit",
      "module": "risk-interest-rate",
      "status": "passed",
      "duration": 0.12,
      "details": {
        "files_checked": ["package.json", "README.md"],
        "package_json_valid": true
      }
    }
  ]
}
```

### Markdown Summary

A human-readable summary is saved to `test_summary.md`:

```markdown
# Integration Test Results

## Summary

- **Total Tests**: 53
- **Passed**: 53
- **Failed**: 0
- **Success Rate**: 100.0%
- **Total Duration**: 8.24s

## Test Results by Module

### risk-interest-rate
- **Tests**: 3
- **Passed**: 3
- **Failed**: 0
- **Success Rate**: 100.0%
```

## Adding New Tests

### 1. Extend the Framework

Add new test methods to the appropriate tester class:

```python
class RiskModelTester(ModuleTester):
    async def test_new_functionality(self) -> TestResult:
        # Your test implementation
        pass
```

### 2. Update Configuration

Add test parameters to `test_config.json`:

```json
{
  "module_configs": {
    "your-module": {
      "test_parameters": {
        "param1": "value1"
      }
    }
  }
}
```

### 3. Register Tests

Add your test to the appropriate test runner method:

```python
async def _run_unit_tests(self) -> List[TestResult]:
    # ... existing tests ...
    
    # Add your new test
    new_test_result = await tester.test_new_functionality()
    results.append(new_test_result)
    
    return results
```

## Continuous Integration

### GitHub Actions

Add to your CI pipeline:

```yaml
- name: Run Integration Tests
  run: |
    cd integration-tests
    python run_tests.py --test-type all
```

### Pre-commit Hooks

Add to your pre-commit configuration:

```yaml
- repo: local
  hooks:
    - id: integration-tests
      name: Integration Tests
      entry: python integration-tests/run_tests.py --test-type unit
      language: system
      pass_filenames: false
```

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   - Ensure all dependencies are installed
   - Check module paths in `test_config.json`
   - Verify Python path includes module directories

2. **Performance Test Failures**
   - Adjust thresholds in `test_config.json`
   - Check system resources
   - Consider running tests in isolation

3. **Workflow Test Timeouts**
   - Increase timeout values in configuration
   - Check for blocking operations
   - Verify async/await usage

### Debug Mode

Run tests with verbose output for debugging:

```bash
python run_tests.py --verbose --test-type unit
```

### Individual Module Testing

Test a specific module:

```python
from test_framework import RiskModelTester

tester = RiskModelTester("risk-interest-rate", "repositories/risk-interest-rate")
result = await tester.test_module_structure()
print(result)
```

## Contributing

1. Follow the existing test structure
2. Add comprehensive test coverage
3. Update documentation
4. Ensure all tests pass
5. Add appropriate error handling

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review test configuration
3. Examine test logs
4. Create an issue with detailed information

---

**Last Updated**: July 2024
**Version**: 1.0.0 