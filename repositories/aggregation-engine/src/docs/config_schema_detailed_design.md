# RADF Config File Schema — Detailed Design

## Purpose
Defines the structure, required fields, and validation rules for the scenario configuration file used by the RADF orchestrator. Ensures all scenarios, dependencies, and aggregations are specified in a clear, extensible, and user-friendly way.

---

## 1. Supported Formats
- YAML (preferred for readability)
- JSON (supported for programmatic use)

---

## 2. Top-Level Structure
```yaml
scenario_name: "<string>"           # Human-readable scenario name
models:
  - name: <string>                  # Model class or plugin name
    id: <string>                    # Unique identifier for this model instance
    depends_on: [<id>, ...]         # (Optional) List of model ids this model depends on
    params:                         # Model-specific parameters (dict)
      ...
aggregation:
  method: <string>                  # Aggregation method (e.g., sum, VaR, ES)
  models: [<id>, ...]               # List of model ids to aggregate
  confidence_level: <float>         # (Optional) For VaR/ES, etc.
  ...                               # (Optional) Other aggregation params
```

---

## 3. Required Fields
- `scenario_name`: Required, string
- `models`: Required, list of model definitions
  - Each model must have:
    - `name`: Required, string (must match a registered model/plugin)
    - `id`: Required, string (unique within scenario)
    - `params`: Required, dict (model-specific)
    - `depends_on`: Optional, list of ids (for dependency graph)
- `aggregation`: Required, dict
  - `method`: Required, string (must match a registered aggregation method)
  - `models`: Required, list of model ids
  - Other fields as required by the aggregation method

---

## 4. Validation Rules
- All model ids must be unique within the scenario
- All `depends_on` references must point to valid model ids
- No circular dependencies (must form a DAG)
- All aggregation model ids must be present in the `models` list
- All required fields must be present; extra fields are allowed for extensibility

---

## 5. Extensibility
- New fields can be added to `params` for model-specific options
- New aggregation methods can add their own required fields
- (Future) Support for scenario-level metadata, user info, etc.

---

## 6. Example Configs

### Simple Two-Model Scenario
```yaml
scenario_name: "Simple Interest Rate + Credit"
models:
  - name: HullWhiteOneFactor
    id: hw1f
    params:
      num_paths: 1000
      time_horizon: 1.0
  - name: MertonModel
    id: merton
    depends_on: [hw1f]
    params:
      num_paths: 1000
      time_horizon: 1.0
aggregation:
  method: VaR
  models: [hw1f, merton]
  confidence_level: 0.99
```

### Multi-Model, Multi-Dependency Scenario
```yaml
scenario_name: "Full Portfolio Stress Test"
models:
  - name: HullWhiteOneFactor
    id: ir
    params:
      num_paths: 2000
      time_horizon: 2.0
  - name: GBMModel
    id: equity
    params:
      num_paths: 2000
      time_horizon: 2.0
  - name: MertonModel
    id: credit
    depends_on: [ir, equity]
    params:
      num_paths: 2000
      time_horizon: 2.0
aggregation:
  method: ES
  models: [ir, equity, credit]
  confidence_level: 0.975
```

---

## 7. Review Checklist
- [ ] Is the schema clear, user-friendly, and extensible?
- [ ] Are all required fields and validation rules specified?
- [ ] Do the example configs cover typical and advanced use cases?

---
