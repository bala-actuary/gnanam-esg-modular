# RADF Plugin System — Detailed Design

## Purpose
The plugin system enables easy registration, discovery, and integration of new models and aggregation methods into the RADF, supporting extensibility and modularity.

---

## 1. Model Plugin Registration
- Each model implements a standard interface (e.g., `ModelInterface`)
- Models are registered via:
  - Entry points (set in `pyproject.toml` or `setup.py`)
  - Or a central registry file (Python dict or YAML)
- At runtime, the orchestrator discovers all available models and loads them dynamically

---

## 2. Aggregation Method Registration
- Aggregation methods are registered in a central registry (dict or plugin system)
- Each method implements a function with a standard signature
- New methods can be added by placing a Python file in the `plugins/` directory or registering via entry points

---

## 3. Discovery Mechanism
- At startup, the orchestrator scans for available model and aggregation plugins
- Uses Python's `importlib.metadata` (for entry points) or file system scanning (for plugins directory)
- Validates that each plugin implements the required interface

---

## 4. Interface Requirements
- **Model Plugins:** Must implement `ModelInterface` with required methods (`get_name`, `simulate`, etc.)
- **Aggregation Plugins:** Must implement a function with signature `aggregate_<method>(model_outputs: dict, **kwargs) -> dict`

---

## 5. Extensibility
- New models and aggregation methods can be added without modifying the core RADF code
- Plugins can be distributed as separate Python packages or dropped into the `plugins/` directory
- (Future) Support for versioning and metadata in plugin registration

---

## 6. Example: Registering a New Model Plugin
```python
# In plugins/my_new_model.py
from models.ModelInterface import ModelInterface

class MyNewModel(ModelInterface):
    ...

# In plugins/__init__.py
from .my_new_model import MyNewModel
MODEL_REGISTRY['MyNewModel'] = MyNewModel
```

---

## 7. Review Checklist
- [ ] Is the registration/discovery process clear and robust?
- [ ] Are interface requirements well-defined?
- [ ] Is it easy to add new models/aggregators without changing core code?

---
