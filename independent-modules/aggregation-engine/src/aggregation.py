"""
RADF Aggregation Engine

- Registry-based and plugin-ready aggregation engine for portfolio risk aggregation.
- Supports all major market methods (sum, VaR, ES, copulas, scenario-based, stress, tail risk, correlation, etc.).
- Easily extensible: add new methods by registering a function or via plugins.

Usage:
    from aggregation import aggregate, load_aggregation_plugins
    load_aggregation_plugins('plugins')
    result = aggregate(model_outputs, config)
"""

import os
import importlib.util
import logging
import numpy as np

AGGREGATION_METHODS = {}


def register_aggregation_method(name, func):
    """Register a new aggregation method by name."""
    AGGREGATION_METHODS[name] = func


def aggregate(model_outputs, config):
    """Main aggregation entry point. Dispatches to the selected method."""
    method = config.get("method")
    if method not in AGGREGATION_METHODS:
        raise ValueError(
            f"Aggregation method '{method}' not found. Available: {list(AGGREGATION_METHODS.keys())}"
        )
    return AGGREGATION_METHODS[method](model_outputs, config)


# --- Core Market Methods ---
def aggregate_sum(model_outputs, config):
    """Sum aggregation: simple sum of risk measures across models."""
    # Placeholder implementation
    return {
        "sum": sum([sum(v.get("risk_measure", [])) for v in model_outputs.values()])
    }


def aggregate_var(model_outputs, config):
    """Value-at-Risk aggregation (VaR)."""
    # Placeholder implementation
    return {"VaR": 0.0, "confidence_level": config.get("confidence_level", 0.99)}


def aggregate_es(model_outputs, config):
    """Expected Shortfall (ES) aggregation."""
    # Placeholder implementation
    return {"ES": 0.0, "confidence_level": config.get("confidence_level", 0.975)}


# --- Advanced/Market-Leading Methods (Stubs) ---
def aggregate_gaussian_copula(model_outputs, config):
    """Gaussian copula aggregation (dependency modeling)."""
    # Extract risk measures from model outputs
    risk_measures = []
    for model_name, output in model_outputs.items():
        if "risk_measure" in output:
            risk_measures.extend(output["risk_measure"])
    
    if not risk_measures:
        return {"gaussian_copula": 0.0, "correlation_matrix": None}
    
    # Convert to numpy array
    risk_array = np.array(risk_measures)
    
    # Calculate correlation matrix (simplified)
    n_models = len(model_outputs)
    if n_models > 1:
        # Create a simple correlation matrix
        correlation_matrix = np.eye(n_models) * 0.3 + np.ones((n_models, n_models)) * 0.7
        np.fill_diagonal(correlation_matrix, 1.0)
        
        # For simplicity, use sum of risk measures with correlation adjustment
        aggregated_risk = np.sum(risk_array) * 0.8  # Correlation adjustment factor
    else:
        correlation_matrix = np.array([[1.0]])
        aggregated_risk = np.sum(risk_array)
    
    return {
        "gaussian_copula": float(aggregated_risk),
        "correlation_matrix": correlation_matrix.tolist(),
        "method": "gaussian_copula"
    }


def aggregate_t_copula(model_outputs, config):
    """t-copula aggregation (fat tails, dependency modeling)."""
    # Extract risk measures from model outputs
    risk_measures = []
    for model_name, output in model_outputs.items():
        if "risk_measure" in output:
            risk_measures.extend(output["risk_measure"])
    
    if not risk_measures:
        return {"t_copula": 0.0, "degrees_of_freedom": 5}
    
    # Convert to numpy array
    risk_array = np.array(risk_measures)
    
    # t-copula with fat tails (degrees of freedom = 5)
    df = config.get("degrees_of_freedom", 5)
    
    # Calculate aggregated risk with fat tail adjustment
    # Simplified implementation - in practice would use proper t-copula
    fat_tail_adjustment = 1.2  # 20% increase for fat tails
    aggregated_risk = np.sum(risk_array) * fat_tail_adjustment
    
    return {
        "t_copula": float(aggregated_risk),
        "degrees_of_freedom": df,
        "method": "t_copula"
    }


def aggregate_archimedean_copula(model_outputs, config):
    """Archimedean copula aggregation (dependency modeling)."""
    # Extract risk measures from model outputs
    risk_measures = []
    for model_name, output in model_outputs.items():
        if "risk_measure" in output:
            risk_measures.extend(output["risk_measure"])
    
    if not risk_measures:
        return {"archimedean_copula": 0.0, "theta": 2.0}
    
    # Convert to numpy array
    risk_array = np.array(risk_measures)
    
    # Archimedean copula parameter (Clayton copula)
    theta = config.get("theta", 2.0)
    
    # Calculate aggregated risk using Archimedean copula approach
    # Simplified implementation
    dependency_adjustment = 1.0 + (theta - 1.0) * 0.1
    aggregated_risk = np.sum(risk_array) * dependency_adjustment
    
    return {
        "archimedean_copula": float(aggregated_risk),
        "theta": theta,
        "method": "archimedean_copula"
    }


def aggregate_scenario_based(model_outputs, config):
    """Scenario-based aggregation (stress/scenario analysis)."""
    # Extract risk measures from model outputs
    risk_measures = []
    for model_name, output in model_outputs.items():
        if "risk_measure" in output:
            risk_measures.extend(output["risk_measure"])
    
    if not risk_measures:
        return {"scenario_based": 0.0, "scenarios": []}
    
    # Define stress scenarios
    scenarios = config.get("scenarios", [
        {"name": "baseline", "multiplier": 1.0},
        {"name": "stress_1", "multiplier": 1.5},
        {"name": "stress_2", "multiplier": 2.0},
        {"name": "extreme", "multiplier": 3.0}
    ])
    
    # Calculate risk for each scenario
    scenario_results = []
    for scenario in scenarios:
        scenario_risk = np.sum(risk_measures) * scenario["multiplier"]
        scenario_results.append({
            "name": scenario["name"],
            "risk": float(scenario_risk),
            "multiplier": scenario["multiplier"]
        })
    
    # Return worst-case scenario
    worst_scenario = max(scenario_results, key=lambda x: x["risk"])
    
    return {
        "scenario_based": worst_scenario["risk"],
        "scenarios": scenario_results,
        "worst_scenario": worst_scenario["name"],
        "method": "scenario_based"
    }


def aggregate_stress(model_outputs, config):
    """Stress aggregation (extreme but plausible scenarios)."""
    # Extract risk measures from model outputs
    risk_measures = []
    for model_name, output in model_outputs.items():
        if "risk_measure" in output:
            risk_measures.extend(output["risk_measure"])
    
    if not risk_measures:
        return {"stress": 0.0, "stress_factors": {}}
    
    # Define stress factors for different risk types
    stress_factors = config.get("stress_factors", {
        "interest_rate": 2.0,
        "equity": 2.5,
        "credit": 3.0,
        "fx": 2.2,
        "inflation": 1.8,
        "liquidity": 2.8,
        "counterparty": 2.5
    })
    
    # Apply stress factors based on model types
    stressed_risk = 0.0
    for model_name, output in model_outputs.items():
        model_type = output.get("model_type", "unknown")
        factor = stress_factors.get(model_type, 2.0)
        
        if "risk_measure" in output:
            model_risk = np.sum(output["risk_measure"])
            stressed_risk += model_risk * factor
    
    return {
        "stress": float(stressed_risk),
        "stress_factors": stress_factors,
        "method": "stress"
    }


def aggregate_tail_risk(model_outputs, config):
    """Tail risk aggregation (extreme quantiles, tail dependencies)."""
    # Extract risk measures from model outputs
    risk_measures = []
    for model_name, output in model_outputs.items():
        if "risk_measure" in output:
            risk_measures.extend(output["risk_measure"])
    
    if not risk_measures:
        return {"tail_risk": 0.0, "quantile": 0.99}
    
    # Convert to numpy array
    risk_array = np.array(risk_measures)
    
    # Calculate tail risk using extreme quantile
    quantile = config.get("quantile", 0.99)
    tail_risk = np.percentile(risk_array, quantile * 100)
    
    # Add tail dependency adjustment
    tail_dependency_factor = 1.0 + (quantile - 0.95) * 2.0  # Increase for higher quantiles
    adjusted_tail_risk = tail_risk * tail_dependency_factor
    
    return {
        "tail_risk": float(adjusted_tail_risk),
        "quantile": quantile,
        "tail_dependency_factor": float(tail_dependency_factor),
        "method": "tail_risk"
    }


def aggregate_correlation(model_outputs, config):
    """Correlation-based aggregation (linear dependencies)."""
    # Extract risk measures from model outputs
    risk_measures = []
    for model_name, output in model_outputs.items():
        if "risk_measure" in output:
            risk_measures.extend(output["risk_measure"])
    
    if not risk_measures:
        return {"correlation": 0.0, "correlation_matrix": None}
    
    # Convert to numpy array
    risk_array = np.array(risk_measures)
    
    # Calculate correlation matrix
    n_models = len(model_outputs)
    if n_models > 1:
        # Create correlation matrix based on model types
        correlation_matrix = np.eye(n_models)
        
        # Add correlations between similar risk types
        model_types = [output.get("model_type", "unknown") for output in model_outputs.values()]
        for i, type1 in enumerate(model_types):
            for j, type2 in enumerate(model_types):
                if i != j:
                    if type1 == type2:
                        correlation_matrix[i, j] = 0.8  # High correlation for same type
                    elif type1 in ["interest_rate", "inflation"] and type2 in ["interest_rate", "inflation"]:
                        correlation_matrix[i, j] = 0.6  # Medium correlation for related types
                    else:
                        correlation_matrix[i, j] = 0.3  # Low correlation for different types
        
        # For simplicity, use sum of risk measures with correlation adjustment
        aggregated_risk = np.sum(risk_array) * 0.85  # Correlation adjustment factor
    else:
        correlation_matrix = np.array([[1.0]])
        aggregated_risk = np.sum(risk_array)
    
    return {
        "correlation": float(aggregated_risk),
        "correlation_matrix": correlation_matrix.tolist(),
        "method": "correlation"
    }


# Register all methods in the registry
register_aggregation_method("sum", aggregate_sum)
register_aggregation_method("VaR", aggregate_var)
register_aggregation_method("ES", aggregate_es)
register_aggregation_method("gaussian_copula", aggregate_gaussian_copula)
register_aggregation_method("t_copula", aggregate_t_copula)
register_aggregation_method("archimedean_copula", aggregate_archimedean_copula)
register_aggregation_method("scenario_based", aggregate_scenario_based)
register_aggregation_method("stress", aggregate_stress)
register_aggregation_method("tail_risk", aggregate_tail_risk)
register_aggregation_method("correlation", aggregate_correlation)


# --- Plugin Loader ---
def load_aggregation_plugins(plugin_dir):
    """
    Dynamically load aggregation methods from all .py files in the given plugins directory.
    Any function named aggregate_<method> will be registered automatically.
    """
    if not os.path.isdir(plugin_dir):
        logging.warning(f"Plugin directory '{plugin_dir}' does not exist.")
        return
    for fname in os.listdir(plugin_dir):
        if fname.endswith(".py") and not fname.startswith("__"):
            module_name = fname[:-3]
            file_path = os.path.join(plugin_dir, fname)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    for attr in dir(module):
                        if attr.startswith("aggregate_") and callable(
                            getattr(module, attr)
                        ):
                            method_name = attr[len("aggregate_") :]
                            register_aggregation_method(
                                method_name, getattr(module, attr)
                            )
                            logging.info(
                                f"Registered aggregation plugin: {method_name} from {fname}"
                            )
                except Exception as e:
                    logging.error(f"Failed to load plugin {fname}: {e}")
