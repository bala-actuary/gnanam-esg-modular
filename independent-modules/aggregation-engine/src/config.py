# Configuration management for RADF will be implemented here.

import os
import yaml
import json
import logging
from typing import Dict, Any, List, Set


def load_config(config_path):
    """Load and parse the scenario config file (YAML/JSON)."""
    if not os.path.exists(config_path):
        logging.error(f"Config file not found: {config_path}")
        return None
    try:
        with open(config_path, "r") as f:
            if config_path.endswith((".yaml", ".yml")):
                return yaml.safe_load(f)
            elif config_path.endswith(".json"):
                return json.load(f)
            else:
                logging.error(
                    "Unsupported config file format. Use .yaml, .yml, or .json."
                )
                return None
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return None


def _validate_required_fields(config: Dict[str, Any]) -> bool:
    """Validate that all required top-level fields are present."""
    required_fields = ["scenario_name", "models", "aggregation"]
    for field in required_fields:
        if field not in config:
            logging.error(f"Missing required field in config: {field}")
            return False
    return True


def _validate_models(config: Dict[str, Any]) -> tuple[bool, Set[str]]:
    """Validate models section and return model IDs."""
    model_ids = set()
    models = config.get("models", [])

    if not isinstance(models, list):
        logging.error("Models must be a list")
        return False, set()

    for i, model in enumerate(models):
        if not isinstance(model, dict):
            logging.error(f"Model {i} must be a dictionary")
            return False, set()

        if "id" not in model:
            logging.error(f"Model {i} must have a unique 'id' field")
            return False, set()

        if "name" not in model:
            logging.error(f"Model {i} must have a 'name' field")
            return False, set()

        if "params" not in model:
            logging.error(f"Model {i} must have a 'params' field")
            return False, set()

        if model["id"] in model_ids:
            logging.error(f"Duplicate model id found: {model['id']}")
            return False, set()

        model_ids.add(model["id"])

    return True, model_ids


def _validate_aggregation(config: Dict[str, Any], model_ids: Set[str]) -> bool:
    """Validate aggregation section."""
    agg = config.get("aggregation", {})

    if not isinstance(agg, dict):
        logging.error("Aggregation section must be a dictionary")
        return False

    if "method" not in agg:
        logging.error("Aggregation section must have 'method' field")
        return False

    if "models" not in agg:
        logging.error("Aggregation section must have 'models' field")
        return False

    if not isinstance(agg["models"], list):
        logging.error("Aggregation models must be a list")
        return False

    for mid in agg["models"]:
        if mid not in model_ids:
            logging.error(f"Aggregation references unknown model id: {mid}")
            return False

    return True


def _validate_dependencies(config: Dict[str, Any], model_ids: Set[str]) -> bool:
    """Validate dependency graph (no cycles, valid references)."""
    models = config.get("models", [])

    for model in models:
        if "depends_on" in model:
            deps = model["depends_on"]
            if not isinstance(deps, list):
                logging.error(f"Model {model['id']}: depends_on must be a list")
                return False

            for dep in deps:
                if dep not in model_ids:
                    logging.error(
                        f"Model {model['id']}: depends_on references unknown model {dep}"
                    )
                    return False
                if dep == model["id"]:
                    logging.error(f"Model {model['id']}: cannot depend on itself")
                    return False

    # Check for cycles using simple DFS
    if not _check_dependency_cycles(models):
        logging.error("Circular dependencies detected in model configuration")
        return False

    return True


def _check_dependency_cycles(models: List[Dict[str, Any]]) -> bool:
    """Check for cycles in dependency graph using DFS."""
    visited = set()
    rec_stack = set()

    def has_cycle(model_id: str) -> bool:
        if model_id in rec_stack:
            return True
        if model_id in visited:
            return False

        visited.add(model_id)
        rec_stack.add(model_id)

        # Find the model
        model = next((m for m in models if m["id"] == model_id), None)
        if model and "depends_on" in model:
            for dep in model["depends_on"]:
                if has_cycle(dep):
                    return True

        rec_stack.remove(model_id)
        return False

    for model in models:
        if model["id"] not in visited:
            if has_cycle(model["id"]):
                return False

    return True


def _validate_custom_fields(config: Dict[str, Any]) -> bool:
    """Validate custom fields and extension points."""
    # Allow custom fields at top level
    # Allow custom fields in model params
    # Allow custom fields in aggregation config
    # Log warnings for unknown fields but don't fail validation
    return True


def validate_config(config):
    """Validate the loaded config against schema and rules."""
    if not config:
        logging.error("Config is empty or could not be loaded.")
        return False

    # Step 1: Validate required fields
    if not _validate_required_fields(config):
        return False

    # Step 2: Validate models and get model IDs
    models_valid, model_ids = _validate_models(config)
    if not models_valid:
        return False

    # Step 3: Validate aggregation
    if not _validate_aggregation(config, model_ids):
        return False

    # Step 4: Validate dependencies
    if not _validate_dependencies(config, model_ids):
        return False

    # Step 5: Validate custom fields (extensibility)
    if not _validate_custom_fields(config):
        return False

    logging.info(
        f"Config validation passed for scenario: {config.get('scenario_name', 'unknown')}"
    )
    return True
