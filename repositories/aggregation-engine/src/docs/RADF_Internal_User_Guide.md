# RADF Internal User Guide

## Overview
The Risk Aggregation & Dependency Framework (RADF) is now fully implemented, tested, and documented. This guide provides a high-level overview, usage instructions, and navigation to all key documentation for users and developers.

---

## 1. Getting Started
- For a quick start, see the main project README and the quickstart guide in `docs/guides/quickstart_api.md`.
- To run a scenario, use the CLI or the test harness. Example:
  ```bash
  python run_radf.py --config RiskModels/src/RADF/sample_scenario_valid.yaml
  ```

---

## 2. Core Features
- Modular orchestrator with robust config loading and validation
- Flexible aggregation engine with plugin support
- Comprehensive error handling and audit logging
- Full test harness for scenario validation and reporting

---

## 3. Extension Points
- To add new aggregation methods, models, or plugins, see:
  - [Extension Points Documentation](extension_points_documentation.md)
- All extension points are designed for easy integration and enterprise extensibility.

---

## 4. Performance Optimization
- For profiling, benchmarking, and optimization strategies, see:
  - [Performance Optimization Guide](performance_optimization_guide.md)

---

## 5. Testing & Validation
- All core components are covered by a comprehensive pytest suite.
- Use the test harness (`test_harness.py`) to run and validate scenarios.
- See the [Test Plan](RADF_Test_Plan.md) for details.

---

## 6. Documentation Navigation
- [RADF SRS](RADF_SRS.md)
- [RADF SDD](RADF_SDD.md)
- [RADF Test Plan](RADF_Test_Plan.md)
- [Extension Points Documentation](extension_points_documentation.md)
- [Performance Optimization Guide](performance_optimization_guide.md)
- [Quickstart Guide](../../docs/guides/quickstart_api.md)

---

## 7. Current State
- RADF is enterprise-ready and fully extensible.
- All phases (foundation, core engine, robustness, testing, documentation) are complete.
- The system is ready for integration, extension, and production deployment.

---

For further help, contact the development team or consult the full documentation suite.
