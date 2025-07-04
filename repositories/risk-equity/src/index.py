"""
Equity Risk Module - Main Entry Point

This module provides equity risk models for the Gnanam ESG platform.
"""

from .models.gbm_model.model import GBMModel
from .models.gbm_model.data_structures import GBMInputData, GBMSimulationResult
from .models.gbm_model.formulas import gbm_step

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main classes and functions
__all__ = [
    "GBMModel",
    "GBMInputData",
    "GBMSimulationResult",
    "gbm_step"
]

def get_available_models():
    """Return list of available equity risk models."""
    return ["gbm_model"]

def create_model(model_type: str):
    """Factory function to create equity risk models."""
    if model_type == "gbm_model":
        return GBMModel()
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_model_info(model_type: str):
    """Get information about a specific model."""
    if model_type == "gbm_model":
        return {
            "name": "Geometric Brownian Motion Model",
            "description": "Stochastic model for equity price simulation",
            "parameters": ["initial_price", "expected_return", "volatility", "time_horizon", "num_time_steps", "num_paths"],
            "outputs": ["price_paths", "time_grid"]
        }
    else:
        raise ValueError(f"Unknown model type: {model_type}")

if __name__ == "__main__":
    # Example usage
    print("Equity Risk Module - Example Usage")
    print("=" * 40)
    
    # Create GBM model
    model = GBMModel()
    
    # Define scenario parameters
    scenario_definition = {
        "initial_price": 100.0,
        "expected_return": 0.05,
        "volatility": 0.20,
        "time_horizon": 1.0,
        "num_time_steps": 252,
        "num_paths": 1000
    }
    
    # Simulate price paths
    try:
        simulation_result = model.simulate(scenario_definition)
        print(f"Generated {simulation_result.paths.shape[1]} price paths")
        print(f"Time steps: {len(simulation_result.time_grid)}")
        print(f"Final prices range: {simulation_result.paths[:, -1].min():.2f} - {simulation_result.paths[:, -1].max():.2f}")
        
    except FileNotFoundError:
        print("Input data files not found. Please ensure gbm_parameters.csv exists in the input directory.")
        print("Example data structure:")
        print("- initial_price: 100.0")
        print("- expected_return: 0.05")
        print("- volatility: 0.20")
        print("- time_horizon: 1.0")
        print("- num_time_steps: 252")
        print("- num_paths: 1000")
    except Exception as e:
        print(f"Error during simulation: {e}")
        print("Please check model parameters and dependencies.") 